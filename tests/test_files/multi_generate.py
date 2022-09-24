from gen.gen import *

def searcher(lst):
    trie = change_lst_to_trie(lst)

    def search(string):
        return string_exists_in_trie(trie, string)
    return search

if __name__ == "__main__":
    lst = ["vox", "machina", "fantasma"]
    search_fn = searcher(lst)
    print(search_fn("tomato"))