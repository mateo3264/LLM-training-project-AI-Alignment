from langchain_community.callbacks import get_openai_callback

def get_data_from_openai(f):
    def wrapper(*args, **kwargs):
        with get_openai_callback() as c:
            response = f(*args)
            print(c)
        return response
    return wrapper

def time_taken(f):
    def wrapper(*args, **kwargs):
        initial_time = time.perf_counter()
        f(*args, **kwargs)
        print('Time taken to find the MHAs: ', time.perf_counter() - initial_time)
        return 
    
    return wrapper