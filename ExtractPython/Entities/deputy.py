import requests
import pandas as pd


class Deputy:
    def __init__(self):
        self.base_url = "https://dadosabertos.camara.leg.br/api/v2/"

    def get_deputies(self, authors_df):
        deputies_dict = {}
        unique_uris = authors_df['uri'].unique()

        for author_uri in unique_uris:
            try:
                response = requests.get(author_uri)
                response_data = response.json()['dados']
                author_propositions = authors_df[authors_df['uri'] == author_uri]['proposition_id'].tolist()
                deputy_id = response_data['id']

                if deputy_id not in deputies_dict:
                    deputies_dict[deputy_id] = {
                        'id': deputy_id,
                        'civil_name': response_data['nomeCivil'],
                        'party_initials': response_data['ultimoStatus']['siglaPartido'],
                        'proposition_ids': author_propositions
                    }
                else:
                    deputies_dict[deputy_id]['proposition_ids'].extend(author_propositions)

            except requests.exceptions.RequestException as e:
                print(f"Error fetching data from {author_uri}: {str(e)}")

        for deputy in deputies_dict.values():
            deputy['proposition_ids'] = list(set(deputy['proposition_ids']))

        deputies_df = pd.DataFrame(deputies_dict.values())
        return deputies_df
