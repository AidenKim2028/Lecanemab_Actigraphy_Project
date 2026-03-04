import pandas as pd 
import os 
import glob

class DataLoader:
    def __init__(self, raw_path):
        self.raw_path = raw_path

    def get_files(self):
        """특정 포맷의 파일 리스트만 반환"""
        return sorted(glob.glob(os.path.join(self.raw_path, "*60secDataTable.csv")))

    def load_data(self, file_path):
        """파일을 읽어 데이터프레임과 환자 정보 반환"""
        file_name = os.path.basename(file_path)
        
        # 파일명에서 정보 추출 (AW25209_이상묵 (2025-05-15)60secDataTable.csv)
        # '_'와 ' ('를 기준으로 분리
        p_id = file_name.split('_')[0]
        p_name = file_name.split('_')[1].split(' (')[0]
        
        # 데이터 로드 (헤더 10줄 스킵)
        df = pd.read_csv(file_path, skiprows=10)
        df.columns = [c.strip() for c in df.columns]
        
        # Timestamp 생성 및 인덱스 설정
        df['Timestamp'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
        df.set_index('Timestamp', inplace=True)
        
        # 분석에 필요한 컬럼만 유지 (Vector Magnitude 및 자세 정보)
        cols_to_keep = ['Vector Magnitude', 'Inclinometer Lying']
        return df[cols_to_keep], p_id, p_name