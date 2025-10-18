import pandas as pd
from data_processor import DataProcessor
import traceback

def debug_real_data():
    """실제 데이터로 디버깅"""
    try:
        processor = DataProcessor()
        
        # 실제 CSV 파일이 있다면 로드
        try:
            # 샘플 파일들 확인
            import os
            csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and 'sample' in f]
            print(f"발견된 CSV 파일들: {csv_files}")
            
            if csv_files:
                # 첫 번째 CSV 파일 로드
                csv_file = csv_files[0]
                print(f"로드할 파일: {csv_file}")
                
                # 파일 내용 확인
                df = pd.read_csv(csv_file, encoding='utf-8-sig')
                print(f"파일 내용:")
                print(df.head())
                print(f"컬럼: {df.columns.tolist()}")
                print(f"데이터 타입: {df.dtypes}")
                
                # 각 행별로 처리 테스트
                for idx, row in df.iterrows():
                    print(f"\n--- 행 {idx} 처리 ---")
                    try:
                        student_name = str(row['이름']).strip()
                        print(f"학생 이름: '{student_name}' (타입: {type(student_name)})")
                        
                        student_id = processor._generate_student_id(student_name)
                        print(f"생성된 ID: '{student_id}'")
                        
                        # 오답번호 처리 테스트
                        wrong_answers = processor._parse_wrong_answers(row['오답번호'])
                        print(f"오답번호: {wrong_answers}")
                        
                    except Exception as e:
                        print(f"행 {idx} 처리 오류: {str(e)}")
                        traceback.print_exc()
                        
        except Exception as e:
            print(f"파일 로드 오류: {str(e)}")
            traceback.print_exc()
            
    except Exception as e:
        print(f"전체 오류: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_real_data()

