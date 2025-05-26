import os
import re
from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import pytest

class Movies:
    """
    Analyzing data from movies.csv
    """
    def __init__(self, path_to_the_file: str):
        """
        Укажите здесь все поля, которые, по вашему мнению, вам понадобятся.
        """
        self.file = path_to_the_file


    def dist_by_release(self) -> dict[int, int]:
        """
        Метод возвращает словарь или упорядоченный словарь, где ключами являются годы, а значениями — количество.
        Вам нужно извлечь годы из названий. Отсортируйте их по убыванию количества.
        """
        try:
            release_years = dict()
            lines = self.read_file()
            year_pattern = r"\((\d{4})\)"
            for line in lines:
                match = re.search(year_pattern, line)
                if match:
                    year = match.group(1)
                    release_years[year] = release_years.get(year, 0) + 1

            release_years = dict(sorted(release_years.items(), key=lambda item: item[1], reverse=True))
        except Exception as error:
            print(f'Error Movies.dist_by_release: {error}')
        return release_years


    def dist_by_genres(self) -> dict[str, int]:
        """
        Метод возвращает словарь, в котором ключами являются жанры, а значениями — количество.
        Отсортируйте его по убыванию количества.
        """
        lst = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
               'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
               'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
        try:
            genres = dict()
            lines = self.read_file()
            for line in lines:
                line = line.split(',')[-1].strip().split('|')
                for elem in line:
                    if elem in lst:
                        genres[elem] = genres.get(elem, 0) + 1
                    else:
                        genres['None'] = genres.get('None', 0) + 1
            genres = dict(sorted(genres.items(), key=lambda item: item[1], reverse=True))
        except Exception as error:
            print(f'Error Movies.dist_by_genres: {error}')
        return genres


    def most_genres(self, n: int) -> dict[str, int]:
        """
        Метод возвращает словарь с топ-n фильмами, где ключами являются названия фильмов,
        а значениями — количество жанров фильма. Отсортируйте его по убыванию чисел.
        """
        lst = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
               'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
               'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
        try:
            movies = dict()
            lines = self.read_file()
            for line in lines:
                genres = line.split(',')[-1].strip().split('|')
                movie = line.split(',')[1].strip()
                movies[movie] = len(genres)
            movies = dict(sorted(movies.items(), key=lambda item: item[1], reverse=True))
            movies = dict(list(movies.items())[:n])
        except Exception as error:
            print(f'Error Movies.most_genres: {error}')
        return movies

    def top_genres_in_year(self, n: int) -> dict[int, dict[str, int]]:
        """
        Метод возвращает словарь с топ-n жанрами в каждом году где ключами являются года,
        а значениями топ-n жанров. Отсортируем по убыванию годов и по убыванию количества встреченных жанров.
        """
        try:
            lines = self.read_file()
            year_genres  = dict()
            year_pattern = r"\((\d{4})\)"
            for line in lines:
                elems = line.split(',')[-1].strip().split('|')
                match = re.search(year_pattern, line)
                if match:
                    year = int(match.group(1))
                    year_genres[year] = year_genres.get(year, {})
                    for elem in elems:
                        if elem != '(no genres listed)':
                            year_genres[year][elem] = year_genres[year].get(elem, 0) + 1
            for key in year_genres.keys():
                year_genres[key] = dict(sorted(year_genres[key].items(), key=lambda item: item[1], reverse=True))
                year_genres[key] = dict(list(year_genres[key].items())[:n])
            year_genres = dict(sorted(year_genres.items(), key=lambda item: item[0], reverse=True))
        except Exception as error:
            print(f'Error Movies.top_genres_in_year: {error}')
        return year_genres

    def read_file(self):
        with open(self.file, mode='r', encoding='utf-8') as file:
            next(file)
            for line in file:
                yield line



class Tags:
    """
    Analyzing data from tags.csv
    """
    def __init__(self, path_to_the_file: str):
        """
        Укажите здесь все поля, которые, по вашему мнению, вам понадобятся.
        """
        self.file = path_to_the_file

    def most_words(self, n: int, _a: bool=True) -> dict[str, int]:
        """
        Метод возвращает топ-n тегов с наибольшим количеством слов внутри.
        Это словарь, в котором ключами являются теги, а значениями — количество слов внутри тега.
        Удалите дубликаты. Отсортируйте по убыванию.
        """
        try:
            lines = self.read_file()
            big_tags = dict()
            for line in lines:
                line = line.split(',')[2]
                big_tags[line] = len(line.split(' '))
            big_tags = dict(sorted(big_tags.items(), key=lambda item: item[1], reverse=True))
            if _a:
                big_tags = dict(list(big_tags.items())[:n])
            else:
                big_tags = dict(list(big_tags.items()))
        except Exception as error:
            print(f'Error Tags.most_words: {error}')
        return big_tags

    def longest(self, n: int, _a: bool=True) -> list[str]:
        """
        Метод возвращает n самых длинных тегов по количеству символов.
        Это список тегов. Удалите дубликаты. Отсортируйте по убыванию.
        """
        try:
            lines = self.read_file()
            big_tags = dict()
            for line in lines:
                line = line.split(',')[2]
                big_tags[line] = len(line)
            big_tags = dict(sorted(big_tags.items(), key=lambda item: item[1], reverse=True))
            if _a:
                big_tags = list(big_tags.keys())[:n]
            else:
                big_tags = list(big_tags.items())
        except Exception as error:
            print(f'Error Tags.longest: {error}')
        return big_tags

    def most_words_and_longest(self) -> list[str]:
        """
        Метод возвращает пересечение между тегами с наибольшим количеством слов и
        тегами с наибольшим количеством символов.
        Удалите дубликаты. Это список тегов.
        """
        try:
            dict_word = self.most_words(n=0, _a=False)
            dict_word = dict(self.longest(n=0, _a=False))
            big_tags = dict_word.keys() & dict_word.keys()
            big_tags = list(big_tags)
        except Exception as error:
            print(f'Error Tags.most_words_and_longest: {error}')
        return big_tags

    def most_popular(self, n: int) -> dict[str, int]:
        """
        Метод возвращает самые популярные теги.
        Это словарь, в котором ключами являются теги, а значениями — количество тегов.
        Удалите дубликаты. Отсортируйте по убыванию количества тегов.
        """
        try:
            lines = self.read_file()
            popular_tags = dict()
            for line in lines:
                line = line.split(',')[2]
                popular_tags[line] = popular_tags.get(line, 0) + 1
            popular_tags = dict(sorted(popular_tags.items(), key=lambda item: item[1], reverse=True))
            popular_tags = dict(list(popular_tags.items())[:n])
        except Exception as error:
            print(f'Error Tags.most_popular: {error}')
        return popular_tags

    def tags_with(self, word: str) -> list[str]:
        """
        Метод возвращает все уникальные теги, содержащие слово, переданное в качестве аргумента.
        Удалите дубликаты. Это список тегов. Отсортируйте его по названиям тегов в алфавитном порядке.
        """
        try:
            lines = self.read_file()
            tags_with_word = list()
            for line in lines:
                line = line.split(',')[2]
                if word.lower() in line.lower():
                    tags_with_word.append(line)
            tags_with_word = list(set(tags_with_word))
            tags_with_word.sort()
        except Exception as error:
            print(f'Error Tags.tags_with: {error}')
        return tags_with_word

    def various_films(self, n: int) -> dict[int, int]:
        """
        Метод возвращает топ-n самых разнообразных фильмов (с наибольшим количеством тегов).
        Это словарь, в котором ключами являются id фильма, а значениями количество тегов этих фильмов.
        """
        try:
            lines = self.read_file()
            movies_and_tags_cnt = {}
            for line in lines:
                line = line.split(',')
                movie = int(line[1])
                if movie not in movies_and_tags_cnt.keys():
                    movies_and_tags_cnt[movie] = 1
                else:
                    movies_and_tags_cnt[movie] += 1
            movies_and_tags_cnt = dict(sorted(movies_and_tags_cnt.items(), key=lambda item: item[1], reverse=True))
            movies_and_tags_cnt = dict(list(movies_and_tags_cnt.items())[:n])
        except Exception as error:
            print(f"Error Tags.various_films: {error}")
        return movies_and_tags_cnt

    def read_file(self):
        with open(self.file, mode='r', encoding='utf-8') as file:
            next(file)
            for line in file:
                yield line



class Ratings:
    """
    Analyzing data from ratings.csv
    """
    def __init__(self, path_to_the_file1: str, path_to_the_file2: str):
        """
        Укажите здесь все поля, которые, по вашему мнению, вам понадобятся.
        """
        self.movies = self.Movies(self, path_to_the_file1, path_to_the_file2)
        self.users = self.Users(self, path_to_the_file1)

    def read_file(self, filename: str):
        with open(filename, "r", encoding='utf-8') as file:
            next(file)
            for line in file:
                yield line

    class Movies():
        def __init__(self, outer_class, file1: str, file2: str):
            self.outer_class = outer_class
            self.file1 = file1
            self.file2 = file2

        def dist_by_year(self) -> dict[int, int]:
            """
            Метод возвращает словарь, в котором ключами являются годы, а значениями — подсчёты.
            Отсортируйте его по годам в порядке возрастания. Вам нужно извлечь годы из временных меток.
            """
            try:
                seconds_in_year = 31557600
                ratings_by_year = {}
                lines = self.outer_class.read_file(self.file1)
                for line in lines:
                    line = line.split(',')
                    years = int((int(line[3]) / seconds_in_year)) + 1970
                    if years not in ratings_by_year.keys():
                        ratings_by_year[years] = 1
                    else:
                        ratings_by_year[years] += 1
                ratings_by_year = dict(sorted(ratings_by_year.items(), key=lambda item: item[0]))
            except Exception as error:
                print(f"Error Ratings.Movies.dist_by_year: {error}")
            return ratings_by_year

        def dist_by_rating(self, _n: int=2) -> dict[float, int]:
            """
            Метод возвращает словарь, в котором ключами являются оценки, а значениями — количество оценок.
            Отсортируйте его по возрастанию оценок.
            """
            try:
                ratings_distribution = {}
                lines = self.outer_class.read_file(self.file1)
                for line in lines:
                    line = line.split(',')
                    if _n == 2:
                        rating = float(line[_n])
                    elif _n == 0:
                        rating = int(line[_n])
                    if rating not in ratings_distribution.keys():
                        ratings_distribution[rating] = 1
                    else:
                        ratings_distribution[rating] += 1
                ratings_distribution = dict(sorted(ratings_distribution.items(), key=lambda item: item[0]))
            except Exception as error:
                print(f"Erorr Ratings.Movies.dist_by_rating: {error}")
            return ratings_distribution

        def top_by_num_of_ratings(self, n: int) -> dict[str, int]:
            """
            Метод возвращает топ-n фильмов по количеству оценок.
            Это словарь, в котором ключами являются названия фильмов, а значениями — числа.
            Отсортируйте его по убыванию чисел.
            """
            try:
                id_and_name = {}
                lines2 = self.outer_class.read_file(self.file2)
                for line in lines2:
                    if '"' in line:
                        line = line.split('"')
                    else:
                        line = line.split(',')
                    id_and_name[int(line[0].strip(','))] = line[1]
                id_and_count = {}
                lines1 = self.outer_class.read_file(self.file1)
                for line in lines1:
                    line = line.split(',')
                    id_movie = int(line[1])
                    if id_movie not in id_and_count.keys():
                        id_and_count[id_movie] = 1
                    else:
                        id_and_count[id_movie] += 1
                name_and_count = {}
                for movie_id, count in id_and_count.items():
                    name_and_count[id_and_name[movie_id]] = count
                name_and_count = dict(sorted(name_and_count.items(), key=lambda item: item[1], reverse=True))
                top_movies = dict(list(name_and_count.items())[:n])
            except Exception as error:
                print(f"Error Ratings.Movies.top_by_num_of_ratings: {error}")
            return top_movies

        def top_by_ratings(self, n: int, metric: str='average', _usr_flag: bool=False, _ind: int=1) -> dict[str, float]:
            """
            Метод возвращает топ-n фильмов по среднему или медианному значению рейтинга.
            Это словарь, в котором ключами являются названия фильмов, а значениями — метрические показатели.
            Отсортируйте его по метрическим показателям в порядке убывания.
            Значения должны быть округлены до 2 знаков после запятой.
            """
            try:
                if not _usr_flag:
                    id_and_name = {}
                    top_movies = []
                    lines2 = self.outer_class.read_file(self.file2)
                    for line in lines2:
                        if '"' in line:
                            line = line.split('"')
                        else:
                            line = line.split(',')
                        id_and_name[int(line[0].strip(','))] = line[1]
                id_and_ratings = {}
                lines1 = self.outer_class.read_file(self.file1)
                for line in lines1:
                    line = line.split(',')
                    movie_id = int(line[_ind])
                    movie_rating = float(line[2])
                    if movie_id not in id_and_ratings.keys():
                        id_and_ratings[movie_id] = [movie_rating]
                    else:
                        id_and_ratings[movie_id].append(movie_rating)
                for key, value in id_and_ratings.items():
                    result = 0
                    if metric == 'average':
                        result = sum(value) / len(value)
                    elif metric == 'median':
                        length = len(value)
                        if len(value) % 2 == 0:
                            result = (value[int(length / 2)] + value[int((length - 1) / 2)]) / 2
                        else:
                            result = value[int(length / 2)]
                    id_and_ratings[key] = round(result, 2)
                if _usr_flag:
                    return id_and_ratings
                name_and_avrg_rating = {}
                for aidi, avrg in id_and_ratings.items():
                    name_and_avrg_rating[id_and_name[aidi]] = avrg
                top_movies = dict(sorted(name_and_avrg_rating.items(), key=lambda item: item[1], reverse=True))
                top_movies = dict(list(top_movies.items())[:n])
            except Exception as error:
                print(f"Error Ratings.Movies.top_by_ratings: {error}")
            return top_movies

        def top_controversial(self, n: int, _usr_flag: bool=False, _ind: int=1) -> dict[str, float]:
            """
            Метод возвращает топ-n фильмов по разбросу оценок.
            Это словарь, в котором ключами являются названия фильмов, а значениями — разброс оценок.
            Отсортируйте его по убыванию разбросов.
            Значения должны быть округлены до 2 знаков после запятой.
            """
            try:
                top_movies = []
                if not _usr_flag:
                    id_and_name = {}
                    lines2 = self.outer_class.read_file(self.file2)
                    for line in lines2:
                        if '"' in line:
                            line = line.split('"')
                        else:
                            line = line.split(',')
                        id_and_name[int(line[0].strip(','))] = line[1]
                id_and_ratings = {}
                lines1 = self.outer_class.read_file(self.file1)
                for line in lines1:
                    line = line.split(',')
                    movie_id = int(line[_ind])
                    movie_rating = float(line[2])
                    if movie_id not in id_and_ratings.keys():
                        id_and_ratings[movie_id] = [movie_rating]
                    else:
                        id_and_ratings[movie_id].append(movie_rating)
                for key, value in id_and_ratings.items():
                    result = 0
                    if len(value) > 1:
                        result = max(value) - min(value)
                    id_and_ratings[key] = result
                if not _usr_flag:
                    name_and_var_rating = {}
                    for aidi, avrg in id_and_ratings.items():
                        name_and_var_rating[id_and_name[aidi]] = avrg
                else:
                    name_and_var_rating = id_and_ratings
                top_movies = dict(sorted(name_and_var_rating.items(), key=lambda item: item[1], reverse=True))
                top_movies = dict(list(top_movies.items())[:n])
            except Exception as error:
                print(f"Error Ratings.Movies.top_controversial: {error}")
            return top_movies

        def top_years(self, n: int) -> dict:
            """
            Метод возвращает топ-n годов с самыми высокими рейтингами.
            Это словарь, в котором ключами являются года, а значениями — средний рейтинг.
            """
            try:
                years_and_ratings = {}
                seconds_in_year = 31557600
                lines = self.outer_class.read_file(self.file1)
                for line in lines:
                    line = line.split(',')
                    year = int(int(line[3]) / seconds_in_year) + 1970
                    if year not in years_and_ratings.keys():
                        years_and_ratings[year] = [float(line[2])]
                    else:
                        years_and_ratings[year].append(float(line[2]))
                for key, value in years_and_ratings.items():
                    years_and_ratings[key] = round((sum(value) / len(value)), 2)
                years_and_ratings = dict(sorted(years_and_ratings.items(), key=lambda item: item[1], reverse=True))
                years_and_ratings = dict(list(years_and_ratings.items())[:n])
            except Exception as error:
                print(f"Error Ratings.Movies.top_years: {error}")
            return years_and_ratings

    class Users(Movies):
        def __init__(self, outer_class, file1):
            self.outer_class = outer_class
            self.file1 = file1

        def dist_by_users(self) -> dict[int, int]:
            """
            Возвращает распределение пользователей по количеству выставленных ими оценок.
            """
            return self.dist_by_rating(0)

        def dist_by_avrg_ratings(self, n: int, metric: str='average') -> dict[int, float]:
            """
            Возвращает распределение пользователей по средним или медианным оценкам, выставленным ими.
            """
            return self.top_by_ratings(n, metric, True, 0)

        def top_users_controversial(self, n: int) -> dict[int, str]:
            """
            Возвращает топ-n пользователей с наибольшей разницей в оценках.
            """
            return self.top_controversial(n, True, 0)



class Links:
    """
    Analyzing data from links.csv
    """
    def __init__(self, path_to_the_file: str):
        """
        Укажите здесь все поля, которые, по вашему мнению, вам понадобятся.
        """
        self.file = path_to_the_file
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_imdb(self, list_of_movies: list[int], list_of_fields: list[str]) -> list[list]:
        """
        Метод возвращает список списков [movieId, поле1, поле2, поле3, ...] для списка фильмов,
        переданного в качестве аргумента (movieId).
        Например, [movieId, режиссёр, бюджет, совокупный мировой доход, продолжительность].
        Значения должны быть получены с веб-страниц фильмов на IMDB.
        Отсортируйте их по убыванию movieId.
        """
        try:
            list_of_movies.sort()
            lines = self.read_file(self.file)
            imdb_info = []
            imdbId = dict()
            count = 0
            for line in lines:
                line = line.split(',')
                for elem in list_of_movies:
                    if elem == int(line[0]):
                        imdbId[line[1]] = elem
                        count += 1
                    if count == len(list_of_movies):
                        break
            for elem in imdbId.keys():
                info = []
                info.append(imdbId[elem])
                response = requests.get(f'http://www.imdb.com/title/tt{elem}/', headers=self.headers)
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                block = soup.find('div', {'class': 'sc-70a366cc-3'})
                block = block.find_all('li', {'data-testid': 'title-pc-principal-credit'})
                for field in list_of_fields:
                    if field == 'director':
                        director = block[0].find('a').text.strip()
                        info.append(director)
                    elif field == 'writer':
                        writer = block[1].find('ul')
                        writer = writer.find_all('a')
                        if len(writer) != 1:
                            info.append([item.text.strip() for item in writer])
                        else:
                            info.append(writer[0].text.strip())
                block = soup.find('ul', {'class': 'sc-db2ddaec-0'})
                block = block.find_all('li', {'class': 'sc-db2ddaec-2'})
                for field in list_of_fields:
                    if field == 'budget':
                        budget = block[0].find('span', {'class': 'ipc-metadata-list-item__list-content-item'}).text.split(' ')[0].strip()
                        info.append(budget)
                    elif field == 'gross worldwide':
                        gross_worldwide = block[3].find('span', {'class': 'ipc-metadata-list-item__list-content-item'}).text.split(' ')[0].strip()
                        info.append(gross_worldwide)
                runtime = soup.find('li', {'data-testid':'title-techspec_runtime'})
                for field in list_of_fields:
                    if field == 'runtime':
                        runtime = runtime.find('div').text.strip()
                        info.append(runtime)
                imdb_info.append(info)
        except Exception as error:
            print(f'Error Links.get_imdb: {error}')
        return imdb_info

    def top_directors(self, n: int) -> dict[str, int]:
        """
        Метод возвращает словарь с топ-n режиссёрами, где ключами являются режиссёры,
        а значениями — количество созданных ими фильмов.
        Отсортируйте его по убыванию значений.
        """
        try:
            self.loading_data('title.crew.tsv.gz')
            directors = defaultdict(int)
            lines = self.read_file(f'{os.getcwd()}\\title.crew.tsv')
            for line in lines:
                line = line.split('\t')[1]
                if line != r'\N':
                    for director in line.split(','):
                        directors[director] += 1
            directors = dict(sorted(directors.items(), key=lambda item: item[1], reverse=True))
            directors = dict(list(directors.items())[:n])
            lst = list(directors.keys())
            for id_director in lst:
                response = requests.get(f'https://www.imdb.com/name/{id_director}/', headers=self.headers)
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                name_director = soup.find('span', {'class': 'hero__primary-text'}).text.strip()
                directors[name_director] = directors.pop(id_director)
        except Exception as error:
            print(f'Error Links.top_directors: {error}')
        return directors

    def most_expensive(self, n: int, len_data: int) -> dict[str, str]:
        """
        Метод возвращает словарь с топ-n фильмами, где ключами являются названия фильмов,
        а значениями — их бюджеты.
        Отсортируйте его по убыванию бюджетов.
        """
        try:
            lines = self.read_file(self.file)
            imdbId = []
            for line in lines:
                imdbId.append(line.split(',')[1])
            budgets = dict()
            for elem in imdbId[:len_data]:
                try:
                    response = requests.get(f'http://www.imdb.com/title/tt{elem}/', headers=self.headers)
                    html_content = response.text
                    soup = BeautifulSoup(html_content, 'html.parser')
                    moviename = soup.find('span', {'class': 'hero__primary-text'}).text.strip()
                    block = soup.find('ul', {'class': 'sc-db2ddaec-0'})
                    block = block.find_all('li', {'class': 'sc-db2ddaec-2'})
                    budget = block[0].find('span', {'class': 'ipc-metadata-list-item__list-content-item'}).text.split(' ')[0].strip()
                    budgets[moviename] = budget
                except Exception as error:
                    print(f'Error Links.most_expensive link: {error}')
            budgets = dict(sorted(budgets.items(), key=lambda item: item[1], reverse=True))
            budgets = dict(list(budgets.items())[:n])
        except Exception as error:
            print(f'Error Links.most_expensive: {error}')
        return budgets

    def most_profitable(self, n: int, len_data: int) -> dict[str, int]:
        """
        Метод возвращает словарь с топ-n фильмами, где ключами являются названия фильмов,
        а значениями — разница между совокупным мировым доходом и бюджетом.
        Отсортируйте его по убыванию разницы.
        """
        try:
            lines = self.read_file(self.file)
            imdbId = []
            for line in lines:
                imdbId.append(line.split(',')[1])
            profits = dict()
            for elem in imdbId[:len_data]:
                try:
                    response = requests.get(f'http://www.imdb.com/title/tt{elem}/', headers=self.headers)
                    html_content = response.text
                    soup = BeautifulSoup(html_content, 'html.parser')

                    moviename = soup.find('span', {'class': 'hero__primary-text'}).text.strip()

                    block = soup.find('ul', {'class': 'sc-db2ddaec-0'})
                    block = block.find_all('li', {'class': 'sc-db2ddaec-2'})

                    budget = block[0].find('span', {'class': 'ipc-metadata-list-item__list-content-item'}).text.split(' ')[0].strip()
                    budget = budget.replace('$','').replace(',','')
                    profit = block[3].find('span', {'class': 'ipc-metadata-list-item__list-content-item'}).text.split(' ')[0].strip()
                    profit = profit.replace('$','').replace(',','')

                    profits[moviename] = int(profit) - int(budget)
                except Exception as error:
                    print(f'Error Links.most_profitable link: {error}')
            profits = dict(sorted(profits.items(), key=lambda item: item[1], reverse=True))
            profits = dict(list(profits.items())[:n])
        except Exception as error:
            print(f'Error Links.most_profitable: {error}')
        return profits

    def longes(self, n: int, len_data: int) -> dict[str, str]:
        """
        Метод возвращает словарь с топ-n фильмами, где ключами являются названия фильмов,
        а значениями — время их просмотра. Если есть несколько версий — выберите любую.
        Отсортируйте их по убыванию времени просмотра.
        """
        try:
            lines = self.read_file(self.file)
            imdbId = []
            for line in lines:
                imdbId.append(line.split(',')[1])
            runtimes = dict()
            for elem in imdbId[:len_data]:
                try:
                    response = requests.get(f'http://www.imdb.com/title/tt{elem}/', headers=self.headers)
                    html_content = response.text
                    soup = BeautifulSoup(html_content, 'html.parser')

                    moviename = soup.find('span', {'class': 'hero__primary-text'}).text.strip()
                    runtime = soup.find('li', {'data-testid':'title-techspec_runtime'})
                    runtime = runtime.find('div').text.strip()

                    runtimes[moviename] = runtime
                except Exception as error:
                    print(f'Error Links.longes link: {error}')
            runtimes = dict(sorted(runtimes.items(), key=lambda item: int(item[1].split(' ')[0])*60+int(item[1].split(' ')[2]), reverse=True))
            runtimes = dict(list(runtimes.items())[:n])
        except Exception as error:
            print(f'Error Links.longes: {error}')
        return runtimes

    def top_cost_per_minute(self, n: int, len_data: int) -> dict[str, int]:
        """
        Метод возвращает словарь с топ-n фильмами, где ключами являются названия фильмов, а
        значениями — бюджеты, разделённые на продолжительность их показа. Бюджеты могут быть в разных валютах — не обращайте на это внимания.
        Значения должны быть округлены до 2 знаков после запятой. Отсортируйте их по убыванию.
        """
        try:
            lines = self.read_file(self.file)
            imdbId = []
            for line in lines:
                imdbId.append(line.split(',')[1])
            costs = dict()
            for elem in imdbId[:len_data]:
                try:
                    response = requests.get(f'http://www.imdb.com/title/tt{elem}/', headers=self.headers)
                    html_content = response.text
                    soup = BeautifulSoup(html_content, 'html.parser')
                    moviename = soup.find('span', {'class': 'hero__primary-text'}).text.strip()
                    block = soup.find('ul', {'class': 'sc-db2ddaec-0'})
                    block = block.find_all('li', {'class': 'sc-db2ddaec-2'})
                    budget = block[0].find('span', {'class': 'ipc-metadata-list-item__list-content-item'}).text.split(' ')[0].strip()
                    budget = budget.replace('$','').replace(',','')
                    runtime = soup.find('li', {'data-testid':'title-techspec_runtime'})
                    runtime = runtime.find('div').text.strip()
                    runtime = runtime.split(' ')
                    runtime = int(runtime[0])*60 + int(runtime[2])
                    costs[moviename] = round(int(budget) / runtime, 2)
                except Exception as error:
                    print(f'Error Links.top_cost_per_minute link: {error}')
            costs = dict(sorted(costs.items(), key=lambda item: item[1], reverse=True))
            costs = dict(list(costs.items())[:n])
        except Exception as error:
            print(f'Error Links.top_cost_per_minute: {error}')
        return costs

    def read_file(self, filename: str):
        with open(filename, mode='r', encoding='utf-8') as file:
            next(file)
            for line in file:
                yield line

    def loading_data(self, data_file: str):
        try:
            if not os.path.exists(f'{os.getcwd()}\\{data_file}'):
                response = requests.get(f'https://datasets.imdbws.com/{data_file}')
                with open(data_file, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                data_file = f'{os.getcwd()}\\{data_file}'
                command = f'7z x {data_file}'
                os.system(command)
        except Exception as error:
            print(f'Error Links.loading_data: {error}')

class Tests():
    def ratings_tests(self):
        exmpl = Ratings('./data/ratings.csv', './data/movies.csv')
        dist_by_year_test = exmpl.movies.dist_by_year()
        assert isinstance(dist_by_year_test, dict)  #проверка на тип данных
        assert all(isinstance(key, int) for key in dist_by_year_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, int) for value in dist_by_year_test.values()) #проверка на тип данных значений
        assert dist_by_year_test == dict(sorted(dist_by_year_test.items(), key=lambda item: item[0])) #проверка на правильную сортировку

        exmpl1 = Ratings('./data/ratings.csv', './data/movies.csv')
        dist_by_rating_test = exmpl1.movies.dist_by_rating()
        assert isinstance(dist_by_rating_test, dict)  #проверка на тип данных
        assert all(isinstance(key, float) for key in dist_by_rating_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, int) for value in dist_by_rating_test.values()) #проверка на тип данных значений
        assert dist_by_rating_test == dict(sorted(dist_by_rating_test.items(), key=lambda item: item[0])) #проверка на правильную сортировку

        exmpl2 = Ratings('./data/ratings.csv', './data/movies.csv')
        top_by_num_of_ratings_test = exmpl2.movies.top_by_num_of_ratings(5)
        assert isinstance(top_by_num_of_ratings_test, dict)  #проверка на тип данных
        assert all(isinstance(key, str) for key in top_by_num_of_ratings_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, int) for value in top_by_num_of_ratings_test.values()) #проверка на тип данных значений
        assert top_by_num_of_ratings_test == dict(sorted(top_by_num_of_ratings_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку

        exmpl3 = Ratings('./data/ratings.csv', './data/movies.csv')
        top_by_ratings_test = exmpl3.movies.top_by_ratings(5)
        assert isinstance(top_by_ratings_test, dict)  #проверка на тип данных
        assert all(isinstance(key, str) for key in top_by_ratings_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, float) for value in top_by_ratings_test.values()) #проверка на тип данных значений
        assert top_by_ratings_test == dict(sorted(top_by_ratings_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку

        exmpl4 = Ratings('./data/ratings.csv', './data/movies.csv')
        top_controversial_test = exmpl4.movies.top_controversial(5)
        assert isinstance(top_controversial_test, dict)  #проверка на тип данных
        assert all(isinstance(key, str) for key in top_controversial_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, float) for value in top_controversial_test.values()) #проверка на тип данных значений
        assert top_controversial_test == dict(sorted(top_controversial_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку

        exmpl5 = Ratings('./data/ratings.csv', './data/movies.csv')
        dist_by_users_test = exmpl5.users.dist_by_users()
        assert isinstance(dist_by_users_test, dict)  #проверка на тип данных
        assert all(isinstance(key, int) for key in dist_by_users_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, int) for value in dist_by_users_test.values()) #проверка на тип данных значений
        assert dist_by_users_test == dict(sorted(dist_by_users_test.items(), key=lambda item: item[0])) #проверка на правильную сортировку

        exmpl6 = Ratings('./data/ratings.csv', './data/movies.csv')
        dist_by_avrg_ratings_test = exmpl6.users.dist_by_avrg_ratings(5)
        assert isinstance(dist_by_avrg_ratings_test, dict)  #проверка на тип данных
        assert all(isinstance(key, int) for key in dist_by_avrg_ratings_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, float) for value in dist_by_avrg_ratings_test.values()) #проверка на тип данных значений
        assert dist_by_avrg_ratings_test == dict(sorted(dist_by_avrg_ratings_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку

        exmpl7 = Ratings('./data/ratings.csv', './data/movies.csv')
        top_controversial_test = exmpl7.users.top_users_controversial(5)
        assert isinstance(top_controversial_test, dict)  #проверка на тип данных
        assert all(isinstance(key, int) for key in top_controversial_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, float) for value in top_controversial_test.values()) #проверка на тип данных значений
        assert top_controversial_test == dict(sorted(top_controversial_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку

        exmpl8 = Ratings('./data/ratings.csv', './data/movies.csv')
        top_years_test = exmpl8.users.top_years(5)
        assert isinstance(top_years_test, dict)  #проверка на тип данных
        assert all(isinstance(key, int) for key in top_years_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, float) for value in top_years_test.values()) #проверка на тип данных значений
        assert top_years_test == dict(sorted(top_years_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку

    def movies_tests(self):
        exmpl = Movies('./data/movies.csv')

        dist_by_release_test = exmpl.dist_by_release()
        assert isinstance(dist_by_release_test, dict)  #проверка на тип данных
        assert all(isinstance(key, str) for key in dist_by_release_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, int) for value in dist_by_release_test.values()) #проверка на тип данных значений
        assert dist_by_release_test == dict(sorted(dist_by_release_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку

        dist_by_release_test = exmpl.dist_by_genres()
        assert isinstance(dist_by_release_test, dict)  #проверка на тип данных
        assert all(isinstance(key, str) for key in dist_by_release_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, int) for value in dist_by_release_test.values()) #проверка на тип данных значений
        assert dist_by_release_test == dict(sorted(dist_by_release_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку

        most_genres_test = exmpl.most_genres(5)
        assert isinstance(most_genres_test, dict)  #проверка на тип данных
        assert all(isinstance(key, str) for key in most_genres_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, int) for value in most_genres_test.values()) #проверка на тип данных значений
        assert most_genres_test == dict(sorted(most_genres_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку

        top_genres_in_year_test = exmpl.top_genres_in_year(5)
        assert isinstance(top_genres_in_year_test, dict)  #проверка на тип данных
        assert all(isinstance(key, int) for key in top_genres_in_year_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, dict) for value in top_genres_in_year_test.values()) #проверка на тип данных значений
        assert top_genres_in_year_test == dict(sorted(top_genres_in_year_test.items(), key=lambda item: item[0], reverse=True)) #проверка на правильную сортировку

    def tags_tests(self):
        exmpl = Tags('./data/tags.csv')

        most_words_test = exmpl.most_words(5)
        assert isinstance(most_words_test, dict)  #проверка на тип данных
        assert all(isinstance(key, str) for key in most_words_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, int) for value in most_words_test.values()) #проверка на тип данных значений
        assert most_words_test == dict(sorted(most_words_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку

        longest_test = exmpl.longest(5)
        assert isinstance(longest_test, list)  #проверка на тип данных
        assert all(isinstance(i, str) for i in longest_test) #проверка на тип данных элементов
        assert longest_test == sorted(longest_test, key=lambda x: len(x), reverse=True) #проверка на правильную сортировку

        most_words_and_longest_test = exmpl.most_words_and_longest()
        assert isinstance(most_words_and_longest_test, list)  #проверка на тип данных
        assert all(isinstance(i, str) for i in most_words_and_longest_test) #проверка на тип данных элементов

        most_popular_test = exmpl.most_popular(5)
        assert isinstance(most_popular_test, dict)  #проверка на тип данных
        assert all(isinstance(key, str) for key in most_popular_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, int) for value in most_popular_test.values()) #проверка на тип данных значений
        assert most_popular_test == dict(sorted(most_popular_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку

        tags_with_test = exmpl.tags_with('funny')
        assert isinstance(tags_with_test, list)  #проверка на тип данных
        assert all(isinstance(i, str) for i in tags_with_test) #проверка на тип данных элементов
        assert tags_with_test == sorted(tags_with_test) #проверка на правильную сортировку

        various_films_test = exmpl.various_films(5)
        assert isinstance(various_films_test, dict)  #проверка на тип данных
        assert all(isinstance(key, int) for key in various_films_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, int) for value in various_films_test.values()) #проверка на тип данных значений
        assert various_films_test == dict(sorted(various_films_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку

    def links_tests(self):
        exmpl = Links('./data/links.csv')

        get_imdb_test = exmpl.get_imdb([9, 6, 55], ['director', 'budget'])
        assert isinstance(get_imdb_test, list) #проверка на тип данных
        assert all(isinstance(i, list) for i in get_imdb_test) #проверка на тип данных элементов

        top_directors_test = exmpl.top_directors(5)
        assert isinstance(top_directors_test, dict)  #проверка на тип данных
        assert all(isinstance(key, str) for key in top_directors_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, int) for value in top_directors_test.values()) #проверка на тип данных значений
        assert top_directors_test == dict(sorted(top_directors_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку

        most_expensive_test = exmpl.most_expensive(5, 5)
        assert isinstance(most_expensive_test, dict)  #проверка на тип данных
        assert all(isinstance(key, str) for key in most_expensive_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, str) for value in most_expensive_test.values()) #проверка на тип данных значений
        assert most_expensive_test == dict(sorted(most_expensive_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку

        most_profitable_test = exmpl.most_profitable(5, 5)
        assert isinstance(most_profitable_test, dict)  #проверка на тип данных
        assert all(isinstance(key, str) for key in most_profitable_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, int) for value in most_profitable_test.values()) #проверка на тип данных значений
        assert most_profitable_test == dict(sorted(most_profitable_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку

        longes_test = exmpl.longes(5, 5)
        assert isinstance(longes_test, dict)  #проверка на тип данных
        assert all(isinstance(key, str) for key in longes_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, str) for value in longes_test.values()) #проверка на тип данных значений
        assert longes_test == dict(sorted(longes_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку

        top_cost_per_minute_test = exmpl.top_cost_per_minute(5, 5)
        assert isinstance(top_cost_per_minute_test, dict)  #проверка на тип данных
        assert all(isinstance(key, str) for key in top_cost_per_minute_test.keys()) #проверка на тип данных ключей
        assert all(isinstance(value, float) for value in top_cost_per_minute_test.values()) #проверка на тип данных значений
        assert top_cost_per_minute_test == dict(sorted(top_cost_per_minute_test.items(), key=lambda item: item[1], reverse=True)) #проверка на правильную сортировку