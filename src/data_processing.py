import pandas as pd
import bs4


def main():
    converted_data_list = pd.read_html('casts.html')  # TODO: fix ValueError: no tables found
    print(converted_data_list)
    return


if __name__ == "__main__":
    main()
