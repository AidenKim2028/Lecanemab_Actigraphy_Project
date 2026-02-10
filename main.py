from src.loader import DataLoader 

def main(): 
    RAW_DIR = 'data/raw'
    PROCESSED_DIR = 'data/processed'

    loader = DataLoader(RAW_DIR, PROCESSED_DIR) 

    clinical_df = loader.load_clinical_data('clinical_master.xlsx')
    print("\n[Clinical Data Sample]")
    print(clinical_df.head())
    
    print("\n--- Pipeline Setup Successful ---")

if __name__ == "__main__":
    main()