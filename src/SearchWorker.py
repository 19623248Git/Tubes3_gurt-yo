import time
from PySide6.QtCore import QThread, Signal
from ExtractCV import ExtractCV
import os

class SearchWorker(QThread):
    """Worker thread for performing CV search operations."""
    
    # Signals for communication with main thread
    progress_updated = Signal(int, int, str)
    search_completed = Signal(list, float, int, int)
    error_occurred = Signal(str)
    
    def __init__(self, db, search_engine, keywords, algorithm, top_n):
        super().__init__()
        self.db = db
        self.search_engine = search_engine
        self.keywords = [k for k in keywords if k and k.strip()]
        self.algorithm = algorithm
        self.top_n = top_n
        self._is_cancelled = False
    
    def cancel(self):
        """Cancel the search operation."""
        self._is_cancelled = True
    
    def run(self):
        """Main search execution in separate thread."""
        try:
            # print(f"Starting search with {len(self.keywords)} keywords: {self.keywords}")

            start_time = time.time()
            all_applications = self.db.get_all_cv_data()
            total_cvs = len(all_applications)
            results = []
            
            for i, app_data in enumerate(all_applications):
                # print(f"Processing CV {i+1}/{total_cvs}: {app_data}")
                
                # Check if cancelled
                if self._is_cancelled:
                    return
                
                cv_path = app_data.get('cv_path', '')
                first_name = app_data.get('first_name', 'Unknown')
                last_name = app_data.get('last_name', 'User')
                current_name = f"{first_name} {last_name}"
                
                # Check if cv_path exists and is valid
                if not cv_path or not os.path.exists(cv_path):
                    print(f"Skipping invalid CV path: {cv_path}")
                    continue
                
                # Emit progress update
                self.progress_updated.emit(i + 1, total_cvs, current_name)
                
                try:
                    cv_extractor = ExtractCV(cv_path)
                    if not hasattr(cv_extractor, 'get_cleaned_text'):
                        print(f"ExtractCV failed for {cv_path}")
                        continue
                        
                    matched_keywords = {}
                    
                    for keyword in self.keywords:
                        if self._is_cancelled:
                            return
                        
                        try:
                            count = self.search_engine._search(self.algorithm, cv_extractor, keyword)
                            if count > 0:
                                matched_keywords[keyword] = count
                        except Exception as search_error:
                            print(f"Search error for keyword '{keyword}' in {cv_path}: {search_error}")
                            continue
                    
                    if matched_keywords:
                        result_entry = {
                            "detail_id": app_data['detail_id'],
                            "applicant_id": app_data['applicant_id'],
                            "name": current_name,
                            "application_role": app_data['application_role'],
                            "cv_path": cv_path,
                            "matched_keywords": matched_keywords
                        }
                        results.append(result_entry)
                        
                except KeyError as e:
                    print(f"Missing key in app_data: {e}")
                    continue
                
                except Exception as e:
                    # Log individual CV processing errors but continue
                    print(f"Error processing CV {cv_path}: {str(e)}")
                    continue
            
            if not self._is_cancelled:
                runtime_ms = (time.time() - start_time) * 1000
                
                # Sort results and get top N
                results.sort(key=lambda x: sum(x['matched_keywords'].values()), reverse=True)
                final_results = results[:self.top_n]
                
                self.search_completed.emit(final_results, runtime_ms, total_cvs, len(results))
        
        except Exception as e:
            self.error_occurred.emit(str(e))