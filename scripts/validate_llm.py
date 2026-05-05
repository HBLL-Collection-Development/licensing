from ui.backend.llm_api import ModelManager


def main():
    cfg = {'backends':[{'type':'mock','name':'mock1','delay':0},{'type':'llama_socket','name':'ll','host':'127.0.0.1','port':59999}]}
    mgr = ModelManager(cfg)
    print('backends:', mgr.list_backends())
    res = mgr.generate('mock1','m1','hello test')
    print('mock response:', res.get('text')[:50])

if __name__ == '__main__':
    main()
