from .attachment import Photo, Snippet, Video
from .community import PartialCommunity
from .member import PostAuthor


class PostLike:
    """Represents a Weverse Post-Like Object.
    Post-Like Objects refer to the different types of Weverse contents that
    share a similar data structure with each other. Examples of which are posts
    that fall under the categories of `Post`, `Moment`, `Media` and `Live`.

    Inherited by:

    - :class:`Post`
    - :class:`.media.MediaLike`
    - :class:`.media.ImageMedia`
    - :class:`.media.YoutubeMedia`
    - :class:`.media.WeverseMedia`
    - :class:`.live.Live`
    - :class:`.moment.MomentLike`
    - :class:`.moment.Moment`
    - :class:`.moment.OldMoment`

    .. container:: operations

        .. describe:: x == y

            Checks if two post-like objects are equal.

        .. describe:: x != y

            Checks if two post-like objects are not equal.

        .. describe:: hash(x)

            Returns the post-like object's hash.

    Attributes
    ----------
    data: :class:`dict`
        The raw data directly taken from the response generated by Weverse's API.
    id: :class:`int`
        The ID of the post-like object.
    body: :class:`str`
        The body that is displayed on the https://weverse.io website.
        Consider using :attr:`plain_body` if you do not want markdowns
        and unnecessary information.
    plain_body: :class:`str`
        The plain body of the post-like object that does not have markdowns
        and unnecessary information.
    url: :class:`str`
        The URL that leads to the post-like object.
    like_count: :class:`int`
        The number of likes for the post-like object.
    comment_count: :class:`int`
        The number of comments for the post-like object.
    published_at: :class:`int`
        The time the post-like object got created at, in epoch.
    is_bookmarked: :class:`bool`
        Whether the user has bookmarked the post-like object.
    is_locked: :class:`bool`
        UNDETERMINED FUNCTIONALITY: (Has always returned `False`.)
    is_hidden_from_artist: :class:`bool`
        Whether the post-like object is hidden from artists. Will most likely
        ever return `True` in posts posted by non-artists.
    is_membership_only: :class:`bool`
        Whether the post-like object can only be seen by users who have a
        paid membership in the community the post belongs to.
    has_product: :class:`bool`
        UNDETERMINED FUNCTIONALITY: (Has always returned `False`.)
    hashtags: list[:class:`str`]
        The list of hashtags used in the post-like object.
    post_type: :class:`str`
        The post type of the post-like object.
    section_type: :class:`str`
        The section the post-like object falls under.
    author: :class:`.member.PostAuthor`
        The :class:`.member.PostAuthor` object of the author who wrote the post-like object.
    community: :class:`.community.PartialCommunity`
        The :class:`.community.PartialCommunity` object of the community the post-like object
        belongs to.
    like_id: :class:`str` | :class:`None`
        The ID of the like on the post-like object, if the user has liked the post.
    """

    __slots__ = (
        "data",
        "id",
        "body",
        "plain_body",
        "url",
        "like_count",
        "comment_count",
        "published_at",
        "is_bookmarked",
        "is_locked",
        "is_hidden_from_artist",
        "is_membership_only",
        "has_product",
        "hashtags",
        "post_type",
        "section_type",
        "author",
        "community",
        "like_id",
    )

    def __init__(self, data: dict):
        self.data: dict = data
        self.id: str = data["postId"]
        self.body: str = data["body"]
        self.plain_body: str = data["plainBody"]
        self.url: str = data["shareUrl"]
        self.like_count: int = data["emotionCount"]
        self.comment_count: int = data["commentCount"]
        self.published_at: int = data["publishedAt"]
        self.is_bookmarked: bool = data["bookmarked"]
        self.is_locked: bool = data["locked"]
        self.is_hidden_from_artist: bool = data["hideFromArtist"]
        self.is_membership_only: bool = data["membershipOnly"]
        self.has_product: bool = data["hasProduct"]
        self.hashtags: list[str] = data["tags"]
        self.post_type: str = data["postType"]
        self.section_type: str = data["sectionType"]
        self.author: PostAuthor = PostAuthor(data["author"])
        self.community: PartialCommunity = PartialCommunity(data["community"])
        self.like_id: str | None = data.get("viewerEmotionId")

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id

        raise NotImplementedError

    def __hash__(self):
        return hash(self.id)


class Post(PostLike):
    """Represents a Weverse Post. Inherits from :class:`PostLike`.

    Shares the same attributes with :class:`PostLike`.

        .. describe:: str(x)

            Returns the post's plain body.
    """

    def __repr__(self):
        return f"Post post_id={self.id}, body={self.plain_body}"

    def __str__(self):
        return self.plain_body

    @property
    def photos(self) -> list[Photo]:
        """list[:class:`.attachment.Photo`]: A list of :class:`.attachment.Photo`
        objects in the post.
        Returns an empty list if there are no photos.
        """
        if not self.data["attachment"].get("photo"):
            return []

        return [
            Photo(photo_data)
            for photo_data in self.data["attachment"]["photo"].values()
        ]

    @property
    def videos(self) -> list[Video]:
        """list[:class:`.attachment.Video`]: A list of :class:`.attachment.Video`
        objects in the post.
        Returns an empty list if there are no videos.
        """
        if not self.data["attachment"].get("video"):
            return []

        return [
            Video(video_data)
            for video_data in self.data["attachment"]["video"].values()
        ]

    @property
    def snippets(self) -> list[Snippet]:
        """list[:class:`.attachment.Snippet`]: A list of :class:`.attachment.Snippet`
        objects in the post.
        Returns an empty list if there are no snippets.
        """
        if not self.data["attachment"].get("snippet"):
            return []

        return [
            Snippet(snippet_data)
            for snippet_data in self.data["attachment"]["snippet"].values()
        ]
