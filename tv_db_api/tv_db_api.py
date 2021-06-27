from loguru import logger
import requests
import json
from typing import List, Dict


class TVDatabaseApi:

    def __init__(self,
                 api_key: str,
                 shows_to_ignore: List = None,
                 episode_fields: List = None,
                 show_fields: List = None) -> None:
        """

        :param api_key:
        :type api_key:
        :param shows_to_ignore:
        :type shows_to_ignore:
        :param episode_fields:
        :type episode_fields:
        :param show_fields:
        :type show_fields:
        """
        self.class_name = type(self).__name__
        logger.info(f"{self.class_name} initialised")

        if episode_fields is None:
            from config import default_episode_fields
            self.episode_fields = default_episode_fields
        else:
            self.episode_fields = episode_fields

        if show_fields is None:
            from config import default_show_fields
            self.show_fields = default_show_fields
        else:
            self.show_fields = show_fields

        if shows_to_ignore is None:
            self.shows_to_ignore = []
        else:
            self.shows_to_ignore = shows_to_ignore

        self.base_url = "https://api.thetvdb.com"

        self.headers = {
            "Content-Type": "application/json",
            "Accept"      : "application/json"
        }

        self._authenticate(api_key)

    def _authenticate(self, api_key: str) -> None:
        """

        :param api_key: str
        :return: jwt_token
        """

        authentication_string = {
            "apikey": api_key
        }

        auth_url = f"{self.base_url}/login"

        data = requests.post(url=auth_url,
                             data=json.dumps(authentication_string),
                             headers=self.headers)

        if data.status_code == 200:
            jwt_token = data.json()["token"]
            self.headers["Authorization"] = f"Bearer {jwt_token}"
        else:
            logger.error(data.json())
            raise ConnectionError("Authentication unsuccessful")

    def get_api_data(self, api_url: str, params: Dict) -> Dict:
        """

        :param api_url:
        :type api_url: str
        :param params:
        :type params:
        :return:
        :rtype:
        """
        response = requests.get(api_url, params=params, headers=self.headers)
        if response.status_code == 200:
            data = response.json()["data"]
            return data
        else:
            logger.error(f"Error getting data from {api_url}")
            logger.error(response.status_code)
            logger.error(response)

    def search_for_show(self, search_string: str) -> Dict:
        """

        :param search_string:
        :type search_string: str
        :return:
        :rtype:
        """
        search_params = {
            "name": search_string
        }
        search_url = f"{self.base_url}/search/series"
        search_data = self.get_api_data(search_url, search_params)
        return search_data

    def get_episode_data(self, show_id: str) -> List[Dict]:
        """
        :param show_id:
        :return:
        """
        episodes_params = {
            "id": show_id
        }
        episodes_url = f"{self.base_url}/series/{show_id}/episodes"
        episodes_data = self.get_paged_api_data(episodes_url, episodes_params)
        return episodes_data

    def get_paged_api_data(self, api_url: str, params: Dict) -> List[Dict]:
        """

        :param api_url:
        :type api_url:
        :param params:
        :type params:
        :return:
        :rtype:
        """
        response = requests.get(api_url, params=params, headers=self.headers)
        if response.status_code == 200:
            next_page = response.json()["links"]["next"]
            all_data = []
            all_data.append(response.json()["data"])
            while next_page is not None:
                params.update({"page": next_page})
                response = requests.get(api_url, params=params, headers=self.headers)
                next_page = response.json()["links"]["next"]
                all_data.append(response.json()["data"])
            return all_data
        else:
            logger.error(f"Error getting data from {api_url}")
            logger.error(response.status_code)
            logger.error(response)

    def get_show_details(self, show_name: str) -> Dict:
        """

        :param show_name:
        :type show_name:
        :return:
        :rtype:
        """
        all_show_data = self.search_for_show(show_name)
        show_data = {k: all_show_data[0].get(k, None) for k in self.show_fields}
        all_episode_data = self.get_episode_data(all_show_data[0]["id"])
        episode_data = []
        for pages in all_episode_data:
            for data in pages:
                formatted_data = {k: data.get(k, None) for k in self.episode_fields}
                episode_data.append(formatted_data)
        show_data["all_episodes"] = episode_data
        return show_data

    def get_details_for_all_shows(self, all_show_list: List[str]) -> List[Dict]:
        """

        :param all_show_list:
        :type all_show_list:
        :return:
        :rtype:
        """
        all_show_dicts = []
        # Easier to find all column names before inserting into the table.
        for show_name in all_show_list:
            if show_name not in self.shows_to_ignore:
                try:

                    logger.debug('Getting TV DB API info for {}'.format(show_name))
                    show_dict = self.get_show_details(show_name)
                    show_dict["show_name_obj"] = all_show_list
                    all_show_dicts.append(show_dict)
                    logger.debug('TV DB info for {show_name} added'.format(
                        show_name=show_name))

                except Exception as exc:
                    logger.error(f"TVDB error {exc}")
            else:
                logger.debug(f"Ignoring {show_name}")

        return all_show_dicts
