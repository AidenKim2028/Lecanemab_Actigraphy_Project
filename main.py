from src.loader import DataLoader 
from src.analyzer import SleepAnalyzer
import pandas as pd 
import os 

def main(): 
    RAW_DIR = 'data/raw'
    RESULTS_DIR = 'results'

    # 객체 생성
    loader = DataLoader(RAW_DIR)
    analyzer = SleepAnalyzer()
    
    file_list = loader.get_files()
    results = []

    print(f"분석 시작: 총 {len(file_list)}명")

    for file_path in file_list:
        try:
            # 1. 로드
            df, p_id, p_name = loader.load_data(file_path)
            
            # 2. 분석
            metrics = analyzer.calculate_metrics(df)
            
            # 3. 결과 정리
            metrics.update({'Patient_ID': p_id, 'Name': p_name})
            results.append(metrics)
            print(f"✅ 완료: {p_id} {p_name}")
            
        except Exception as e:
            print(f"❌ 오류 발생 ({os.path.basename(file_path)}): {e}")

    # 4. 저장
    if results:
        final_df = pd.DataFrame(results)
        # 컬럼 순서 조정 (ID, 이름 먼저)
        cols = ['Patient_ID', 'Name', 'Sleep_Duration(hr)', 'Average_TST(hr)', 'Sleep_Efficiency(%)', 'Sleep_Fragmentation(wake/hr)', 'SRI', 
                'Interday Stability', 'Amplitude', 'Acrophase(hr)']
        final_df = final_df[cols]
        
        output_file = os.path.join(RESULTS_DIR, 'sleep_analysis_summary.csv')
        final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n 💯 모든 분석 완료! 결과가 {output_file}에 저장되었습니다.")

if __name__ == "__main__":
    main()


