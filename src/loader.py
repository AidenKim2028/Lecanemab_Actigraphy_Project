import pandas as pd 
import os 

class DataLoader: 
    def __init__ (self, raw_path, processed_path): 
        self.raw_path = raw_path
        self.processed_path = processed_path 
    def load_clinical_data(self, file_name):
        """임상 데이터(엑셀) 로드"""
        path = os.path.join(self.raw_path, file_name)
        if not os.path.exists(path):
            print(f"⚠️ 파일이 없습니다: {file_name}. 가짜 데이터를 생성합니다.")
            return self._generate_dummy_clinical()
        return pd.read_excel(path)

    def _generate_dummy_clinical(self):
        """테스트용 가짜 임상 데이터 생성"""
        data = {
            'Patient_ID': ['P01', 'P02', 'P03'],
            'Age': [72, 68, 75],
            'CDR_SB_BL': [0.5, 1.0, 0.5],
            'CDR_SB_18M': [1.0, 1.5, 0.5],
            'APOE4': [1, 0, 1]
        }
        return pd.DataFrame(data)


