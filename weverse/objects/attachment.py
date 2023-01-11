class Photo:
    """Represents a Weverse Photo.

    .. container:: operations

        .. describe:: x == y

            Checks if two photos are equal.

        .. describe:: x != y

            Checks if two photos are not equal.

        .. describe:: hash(x)

            Returns the photo's hash.

        .. describe:: str(x)

            Returns the photo's URL.

    Attributes
    ----------
    data: :class:`dict`
        The raw data directly taken from the response generated by Weverse's API.
    id: :class:`int`
        The ID of the photo.
    url: :class:`str`
        The URL of the photo.
    height: :class:`int`
        The height of the photo.
    width: :class:`int`
        The width of the photo.
    """

    __slots__ = ("data", "id", "url", "height", "width")

    def __init__(self, data: dict):
        self.data: dict = data
        self.id: str = data["photoId"]
        self.url: str = data["url"]
        self.height: int = data["height"]
        self.width: int = data["width"]

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id

        raise NotImplementedError

    def __repr__(self):
        return f"Photo photo_id={self.id}, url={self.url}"

    def __str__(self):
        return self.url

    def __hash__(self):
        return hash(self.id)


class Video:
    """Represents a Weverse Video.

    .. container:: operations

        .. describe:: x == y

            Checks if two videos are equal.

        .. describe:: x != y

            Checks if two videos are not equal.

        .. describe:: hash(x)

            Returns the video's hash.

    Attributes
    ----------
    data: :class:`dict`
        The raw data directly taken from the response generated by Weverse's API.
    id: :class:`int`
        The ID of the video.
    duration: :class:`int`
        The duration of the video, in seconds.
    height: :class:`int`
        The height of the video.
    width: :class:`int`
        The width of the video.
    thumbnail_url: :class:`str`
        The URL of the thumbnail of the video.

    Notes
    -----
    Due to Weverse's implementations, the URL of the video itself is not accessible
    from this object. As a workaround, please make use of the
    :meth:`.WeverseClient.fetch_video_url()` method to make an additional
    API call to fetch the video URL.
    """

    __slots__ = ("data", "id", "duration", "height", "width", "thumbnail_url")

    def __init__(self, data: dict):
        self.data: dict = data
        self.id: str = data["videoId"]
        self.duration: int = data["uploadInfo"]["playTime"]
        self.height: int = data["uploadInfo"]["height"]
        self.width: int = data["uploadInfo"]["width"]
        self.thumbnail_url: str = data["uploadInfo"]["imageUrl"]

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id

        raise NotImplementedError

    def __repr__(self):
        return f"Video video_id={self.id}, duration={self.duration}"

    def __hash__(self):
        return hash(self.id)


class Snippet:
    """Represents a Weverse Snippet. A Snippet can be
    perceived as an embed.

    .. container:: operations

        .. describe:: x == y

            Checks if two snippets are equal.

        .. describe:: x != y

            Checks if two snippets are not equal.

        .. describe:: hash(x)

            Returns the snippet's hash.

        .. describe:: str(x)

            Returns the snippet's title.

    Attributes
    ----------
    data: :class:`dict`
        The raw data directly taken from the response generated by Weverse's API.
    id: :class:`int`
        The ID of the snippet.
    url: :class:`str`
        The URL of the website the snippet brings to.
    title: :class:`str`
        The title of the snippet.
    description: :class:`str`
        The description of the snippet.
    type: :class:`str` | :class:`None`
        The type of snippet it is, if any.
    site: :class:`str` | :class:`None`
        The website of the snippet, if any.
    domain: :class:`str`
        The domain name of the snippet.
    thumbnail_url: :class:`str` | :class:`None`
        The URL of the thumbnail of the snippet, if any.
    """

    __slots__ = (
        "data",
        "id",
        "url",
        "title",
        "description",
        "type",
        "site",
        "domain",
        "thumbnail_url",
    )

    def __init__(self, data: dict):
        self.data: dict = data
        self.id: str = data["snippetId"]
        self.url: str = data["url"]
        self.title: str = data["title"]
        self.description: str = data["description"]
        self.type: str | None = data.get("type")
        self.site: str | None = data.get("site")
        self.domain: str = data["domain"]
        self.thumbnail_url: str | None = (
            data["image"]["url"] if data.get("image") else None
        )

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id

        raise NotImplementedError

    def __repr__(self):
        return f"Snippet snippet_id={self.id} title={self.title}"

    def __str__(self):
        return self.title

    def __hash__(self):
        return hash(self.id)
