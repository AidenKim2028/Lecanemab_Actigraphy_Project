import numpy as np
from scipy.optimize import curve_fit

class SleepAnalyzer:
    def __init__(self, threshold=40):
        self.threshold = threshold # 수면 판단 기준값

    def calculate_metrics(self, df):
        # 수면 판정 (1: 수면, 0: 각성)
        # VM이 낮거나 Lying 시간이 길 때 수면으로 판정
        is_sleep = ((df['Vector Magnitude'] < self.threshold) | (df['Inclinometer Lying'] > 30)).astype(int)
        
        # Sleep Duration (총 수면 시간 - 시간 단위)
        duration_hr = is_sleep.sum() / 60

        # Average TST
        num_days = len(df) / 1440
        avg_tst_hr = duration_hr / num_days 

        # Sleep Efficiency (수면 효율 - %)
        efficiency = (is_sleep.sum() / len(is_sleep)) * 100
        
        # Sleep Fragmentation (수면 분절 - 횟수/시간)
        # 수면 상태에서 각성 상태로 변하는 횟수 계산
        transitions = ((is_sleep.shift(1) == 1) & (is_sleep == 0)).sum()
        fragmentation = (transitions / duration_hr) if duration_hr > 0 else 0
        
        # SRI (Sleep Regularity Index)
        sri = self._calculate_sri(is_sleep.values)

        # IS (Interday Stability)
        is_val = self._calculate_is(df['Vector Magnitude'].values)
        
        # Parametric Circadian Analysis (Cosinor)
        amplitude, acrophase = self._cosinor_analysis(df)

        return {
            'Sleep_Duration(hr)': round(duration_hr, 2),
            'Average_TST(hr)': round(avg_tst_hr, 2),
            'Sleep_Efficiency(%)': round(efficiency, 2),
            'Sleep_Fragmentation(wake/hr)': round(fragmentation, 2),
            'SRI': round(sri, 2),
            'Interday Stability': round(is_val, 3),
            'Amplitude': round(amplitude, 2),
            'Acrophase(hr)': self._format_hours_to_time(acrophase)
        }

    def _calculate_sri(self, sleep_vec):
        """24시간 간격 일치 확률 기반 SRI 계산"""
        day_minutes = 1440
        if len(sleep_vec) <= day_minutes: return np.nan
        
        # 24시간 뒤의 상태와 비교
        matches = (sleep_vec[:-day_minutes] == sleep_vec[day_minutes:]).sum()
        prob = matches / (len(sleep_vec) - day_minutes)
        return 100 * (2 * prob - 1)
    
    def _calculate_is(self, data):
        """일주기 안정성(IS) 계산: 24시간 주기의 일관성 측정"""
        n = len(data)
        p = 1440 # 1일 분량(minutes)
        if n < p: return np.nan
        
        # 데이터를 날짜별로 재구성하여 시간대별 평균 계산
        reshaped = data[:(n // p) * p].reshape(-1, p)
        hourly_averages = np.mean(reshaped, axis=0)
        overall_mean = np.mean(data)
        
        numerator = np.sum((hourly_averages - overall_mean)**2) * (n / p)
        denominator = np.sum((data - overall_mean)**2)
        
        return numerator / denominator if denominator != 0 else 0
    
    def _format_hours_to_time(self, hours):
        if np.isnan(hours): return ""
        h = int(hours)
        m = int(round((hours - h) * 60))
        if m == 60: # 60분이 되면 시간 올림 처리
            h += 1
            m = 0
        return f"{h % 24:02d}:{m:02d}"
    
    def _cosinor_analysis(self, df):
        """코사인 함수를 데이터에 피팅하여 진폭과 위상 계산"""
        # 시간 데이터를 0~24시간 값으로 변환
        t_hours = (df.index - df.index[0]).total_seconds() / 3600
        y_data = df['Vector Magnitude'].values
        
        # 코사인 모델 정의: f(t) = Mesor + Amplitude * cos(2*pi*t/24 + phi)
        def cos_func(t, mesor, amp, phi):
            return mesor + amp * np.cos(2 * np.pi * t / 24 + phi)
        
        try:
            # 초기값 설정 및 피팅
            popt, _ = curve_fit(cos_func, t_hours, y_data, p0=[np.mean(y_data), np.std(y_data), 0])
            mesor, amp, phi = popt
            
            # Acrophase를 시간(0~24) 단위로 변환
            acrophase = (-phi * 24 / (2 * np.pi)) % 24
            return abs(amp), acrophase
        except:
            return np.nan, np.nan