#!/usr/bin/env python3

import requests
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

class NutritionalFacts:
    def __init__(self, api_key, ingredients_list):
        self.api_key = api_key
        self.ingredients_list = ingredients_list
        self.daily_values = self.load_daily_values('data/Daily-Reference-Values.csv')
        self.reference_intakes = self.load_reference_intakes('data/Reference-Daily-Intakes.csv')

    def load_daily_values(self, csv_file):
        return pd.read_csv(csv_file)

    def load_reference_intakes(self, csv_file):
        return pd.read_csv(csv_file)

    def get_nutritional_facts(self):
        if not self.ingredients_list:
            logging.warning("Нет введенных ингредиентов для получения питательных фактов.")
            return {}

        nutrient_info = {}
        for ingredient in self.ingredients_list:
            try:
                search_response = requests.get(f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={self.api_key}&query={ingredient}")

                if search_response.status_code != 200:
                    logging.error(f"Ошибка API для ингредиента '{ingredient}': {search_response.status_code}")
                    nutrient_info[ingredient] = "Ошибка получения данных."
                    continue

                search_data = search_response.json()
                if search_data['foods']:
                    food_id = search_data['foods'][0]['fdcId']
                    details_response = requests.get(f"https://api.nal.usda.gov/fdc/v1/food/{food_id}?api_key={self.api_key}")

                    if details_response.status_code == 200:
                        nutrients = details_response.json().get('foodNutrients', [])
                        formatted_nutrients = {}

                        for nutrient in nutrients:
                            nutrient_name = nutrient.get('nutrient', {}).get('name', 'Неизвестно').split(',')[0].strip()
                            nutrient_amount = nutrient.get('amount', 0)

                            daily_value_row = self.daily_values[self.daily_values['Food Component'].str.contains(nutrient_name, case=False, na=False, regex=False)]
                            reference_value_row = self.reference_intakes[self.reference_intakes['Nutrient'].str.contains(nutrient_name, case=False, na=False, regex=False)]

                            if not daily_value_row.empty:
                                daily_value = daily_value_row['Adults and Children ≥ 4 years'].values[0]
                                percentage_of_daily_value = (nutrient_amount / daily_value) * 100 if daily_value > 0 else 0
                                if nutrient_name.lower() in ['energy', 'protein', 'total lipid (fat)', 'sodium']:
                                    formatted_nutrients[nutrient_name.lower()] = f"{percentage_of_daily_value / 100:.2f}%"
                            elif not reference_value_row.empty:
                                reference_value = reference_value_row['Adults and Children ≥ 4 years'].values[0]
                                percentage_of_reference_value = (nutrient_amount / reference_value) * 100 if reference_value > 0 else 0
                                if nutrient_name.lower() in ['energy', 'protein', 'total lipid (fat)', 'sodium']:
                                    formatted_nutrients[nutrient_name.lower()] = f"{percentage_of_reference_value / 100:.2f}%"

                        nutrient_info[ingredient] = formatted_nutrients
                    else:
                        nutrient_info[ingredient] = "Нет данных о питательных веществах."
                        logging.warning(f"Нет данных о питательных веществах для ингредиента '{ingredient}'.")
                else:
                    nutrient_info[ingredient] = "Нет данных о питательных веществах."
                    logging.warning(f"Нет данных о питательных веществах для ингредиента '{ingredient}'.")
            except Exception as e:
                logging.error(f"Ошибка при получении информации о питательных веществах для {ingredient}: {e}")
                nutrient_info[ingredient] = "Ошибка получения данных."

        return nutrient_info

def load_recipes():
    recipes_df = pd.read_csv('data/epi_r.csv')
    urls_df = pd.read_csv('data/recipes_with_urls.csv')
    ingredients_columns = recipes_df.columns[10:]
    recipes_df['ingredients'] = recipes_df[ingredients_columns].apply(lambda x: ', '.join(x[x > 0].index), axis=1)
    merged_df = pd.merge(recipes_df[['title', 'ingredients']], urls_df, on='title', how='left')
    return merged_df

def filter_recipes_by_ingredients(merged_df, ingredients_input):
    ingredients_list = [ingredient.strip().lower() for ingredient in ingredients_input.split(',')]
    merged_df['match_count'] = merged_df['ingredients'].str.lower().apply(lambda x: sum(x.count(ingredient) for ingredient in ingredients_list))
    filtered_recipes = merged_df[merged_df['match_count'] > 0]
    top_recipes = filtered_recipes.sort_values(by='match_count', ascending=False).head(5)
    return top_recipes[['title', 'url']]

if __name__ == "__main__":
    MY_API_KEY = 'k1sRSzetpO2Ap2ebxR9fn6Zvmc8pYAfqlAfXLge8'

    user_input = input("Введите ингредиенты через запятую: ")
    ingredients = [ingredient.strip() for ingredient in user_input.split(',')]

    nutritional_facts = NutritionalFacts(MY_API_KEY, ingredients)
    facts = nutritional_facts.get_nutritional_facts()

    for ingredient, info in facts.items():
        print(f"Факты о питательных веществах для '{ingredient}':")
        if isinstance(info, dict):
            print("Nutrients:")
            for nutrient, percentage in info.items():
                print(f"- {nutrient}: {percentage}")
        else:
            print(info)
        print()

    merged_df = load_recipes()
    filtered_recipes = filter_recipes_by_ingredients(merged_df, user_input)

    if not filtered_recipes.empty:
        print("\nНайденные рецепты (топ-5):")
        for index, row in filtered_recipes.iterrows():
            print(f"- {row['title'].strip()}: {row['url']}")
    else:
        print("Рецепты не найдены с указанными ингредиентами.")
