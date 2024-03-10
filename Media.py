class Media:
    def __init__(self, article_to_reduce_url, article_div=None, cookie_div=None, media_login_url=None,
                 username=None, password=None, username_id_tag=None, password_id_tag=None):
        self._article_to_reduce_url = article_to_reduce_url
        self._article_div = article_div
        self._cookie_div = cookie_div
        self._media_login_url = media_login_url
        self._username = username
        self._password = password
        self._username_id_tag = username_id_tag
        self._password_id_tag = password_id_tag

    # Accesseurs
    def get_article_to_reduce_url(self):
        return self._article_to_reduce_url

    def get_article_div(self):
        return self._article_div

    def get_cookie_div(self):
        return self._cookie_div

    def get_media_login_url(self):
        return self._media_login_url

    def get_username(self):
        return self._username

    def get_password(self):
        # Attention : Il faut être prudent avec l'exposition des mots de passe.
        return self._password

    def get_username_id_tag(self):
        return self._username_id_tag

    def get_password_id_tag(self):
        return self._password_id_tag

    def __str__(self):
        return (f"Media(article_to_reduce_url={self._article_to_reduce_url}, article_div={self._article_div}, "
                f"cookie_div={self._cookie_div}, media_login_url={self._media_login_url}, username={self._username}, "
                f"password={'******' if self._password else None}, username_id_tag={self._username_id_tag}, "
                f"password_id_tag={self._password_id_tag})")
