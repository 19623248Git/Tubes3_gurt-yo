import time
from PySide6.QtCore import QThread, Signal
from ExtractCV import ExtractCV
import os

class SearchWorker(QThread):
    """Worker thread for performing CV search operations."""
    
    progress_updated = Signal(int, int, str)
    search_completed = Signal(list, dict, int, int)
    error_occurred = Signal(str)
    
    def __init__(self, db, search_engine, keywords, algorithm, top_n):
        super().__init__()
        self.db = db
        self.search_engine = search_engine
        self.algorithm = algorithm
        self.top_n = top_n
        self._is_cancelled = False

        if self.algorithm == 'ac':
            # For AC, we expect the raw, comma-separated string.
            # The ACStrategy itself will handle parsing it.
            self.keywords = keywords 
        else:
            # For KMP/BM, 'keywords' is already a list from main.py
            # We just need to assign it.
            self.keywords = [k for k in keywords if k and k.strip()]
    
    def cancel(self):
        """Cancel the search operation."""
        self._is_cancelled = True
    
    def run(self):
        """Main search execution in separate thread."""
        try:
            start_time = time.time()
            all_applications = self.db.get_all_cv_data()
            total_cvs = len(all_applications)
            results = []
            
            # Timing variables for separate tracking
            exact_start_time = 0
            exact_total_time = 0
            fuzzy_start_time = 0
            fuzzy_total_time = 0
            exact_matches_found = 0
            fuzzy_matches_found = 0
            
            # CV scanning counters
            exact_cvs_scanned = 0
            fuzzy_cvs_scanned = 0
            
            for i, app_data in enumerate(all_applications):
                if self._is_cancelled:
                    return
                
                cv_path = app_data.get('cv_path', '')
                first_name = app_data.get('first_name', 'Unknown')
                last_name = app_data.get('last_name', 'User')
                current_name = f"{first_name} {last_name}"
                
                if not cv_path or not os.path.exists(cv_path):
                    print(f"Skipping invalid CV path: {cv_path}")
                    continue
                
                self.progress_updated.emit(i + 1, total_cvs, current_name)
                
                try:
                    cv_extractor = ExtractCV(cv_path)
                    if not hasattr(cv_extractor, 'get_cleaned_text'):
                        print(f"ExtractCV failed for {cv_path}")
                        continue
                    
                    matched_keywords = {}
                    cv_has_exact_matches = False

                    if self.algorithm == 'ac':
                        # Call AC search ONCE with all keywords
                        ac_strategy = self.search_engine.strategies['ac']
                        total_count = ac_strategy.search(cv_extractor, self.keywords)
                        
                        exact_end_time = time.time()
                        exact_total_time += (exact_end_time - exact_start_time)

                        if total_count > 0:
                            cv_has_exact_matches = True
                            exact_matches_found += total_count
                            # Get detailed results from the side-channel property
                            ac_details = ac_strategy.last_results
                            print(ac_details)
                            for keyword, indices in ac_details.items():
                                matched_keywords[keyword] = {
                                    'count': len(indices),
                                    'type': 'exact'
                                }
                        else:
                            # If AC finds no exact matches, perform fuzzy search for each keyword
                            fuzzy_cvs_scanned += 1
                            individual_keywords = [k.strip() for k in self.keywords.split(',') if k.strip()]
                            for keyword in individual_keywords:
                                if self._is_cancelled:
                                    return
                                
                                fuzzy_start_time = time.time()
                                fuzzy_count = self.search_engine.strategies['fuzzy'].search(cv_extractor, keyword)
                                fuzzy_end_time = time.time()
                                fuzzy_total_time += (fuzzy_end_time - fuzzy_start_time)

                                if fuzzy_count > 0:
                                    matched_keywords[keyword] = {
                                        'count': fuzzy_count,
                                        'type': 'fuzzy'
                                    }
                                    fuzzy_matches_found += fuzzy_count

                    else:
                        for keyword in self.keywords:
                            if self._is_cancelled:
                                return
                            
                            try:
                                # Time exact search
                                exact_start_time = time.time()
                                
                                # Try exact search first (KMP/BM)
                                if self.algorithm == 'kmp':
                                    exact_count = self.search_engine.strategies['kmp'].search(cv_extractor, keyword)
                                elif self.algorithm == 'bm':  # BM
                                    exact_count = self.search_engine.strategies['bm'].search(cv_extractor, keyword)
                                else:
                                    raise ValueError(f"Unsupported algorithm: {self.algorithm}")
                                
                                exact_end_time = time.time()
                                exact_total_time += (exact_end_time - exact_start_time)
                                
                                if exact_count > 0:
                                    # Store with match type information
                                    matched_keywords[keyword] = {
                                        'count': exact_count,
                                        'type': 'exact'
                                    }
                                    exact_matches_found += exact_count
                                    cv_has_exact_matches = True
                                
                                else:
                                    # If no exact matches, try fuzzy search
                                    fuzzy_start_time = time.time()
                                    
                                    fuzzy_count = self.search_engine.strategies['fuzzy'].search(cv_extractor, keyword)
                                    
                                    fuzzy_end_time = time.time()
                                    fuzzy_total_time += (fuzzy_end_time - fuzzy_start_time)
                                    
                                    if fuzzy_count > 0:
                                        # Store with match type information
                                        matched_keywords[keyword] = {
                                            'count': fuzzy_count,
                                            'type': 'fuzzy'
                                        }
                                        fuzzy_matches_found += fuzzy_count
                                        
                            except Exception as search_error:
                                print(f"Search error for keyword '{keyword}' in {cv_path}: {search_error}")
                                continue
                    
                    exact_cvs_scanned += 1
                    
                    if not cv_has_exact_matches:
                        fuzzy_cvs_scanned += 1
                    
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
                    print(f"Error processing CV {cv_path}: {str(e)}")
                    continue
            
            if not self._is_cancelled:
                total_runtime_ms = (time.time() - start_time) * 1000
                exact_time_ms = exact_total_time * 1000
                fuzzy_time_ms = fuzzy_total_time * 1000
                
                results.sort(key=lambda x: sum(match_data['count'] for match_data in x['matched_keywords'].values()), reverse=True)
                final_results = results[:self.top_n]
                
                timing_data = {
                    'exact_time_ms': exact_time_ms,
                    'fuzzy_time_ms': fuzzy_time_ms,
                    'exact_matches': exact_matches_found,
                    'fuzzy_matches': fuzzy_matches_found,
                    'exact_cvs_scanned': exact_cvs_scanned,
                    'fuzzy_cvs_scanned': fuzzy_cvs_scanned,
                    'total_time_ms': total_runtime_ms
                }
                
                self.search_completed.emit(final_results, timing_data, total_cvs, len(results))
        
        except Exception as e:
            self.error_occurred.emit(str(e))