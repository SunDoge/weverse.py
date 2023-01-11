class PartialMember:
    """Represents a Weverse Member with partial information available.

    Inherited by:

    - :class:`Artist`
    - :class:`PostAuthor`
    - :class:`Member`

    .. container:: operations

        .. describe:: x == y

            Checks if two members are equal.

        .. describe:: x != y

            Checks if two members are not equal.

        .. describe:: hash(x)

            Returns the member's hash.

        .. describe:: str(x)

            Returns the member's name.

    Attributes
    ----------
    data: :class:`str`
        The raw data directly taken from the response generated by Weverse's API.
    id: :class:`str`
        The ID of the member.
    name: :class:`str`
        The name of the member.
    image_url: :class:`str` | :class:`None`
        The URL of the profile image of the member, if any.
    profile_type: :class:`str`
        The profile type of the member.
    """

    __slots__ = ("data", "id", "name", "image_url", "profile_type")

    def __init__(self, data: dict):
        self.data: dict = data
        self.id: str = data["memberId"]
        self.name: str = data["profileName"]
        self.image_url: str | None = data.get("profileImageUrl")
        self.profile_type: str = data["profileType"]

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id

        raise NotImplementedError

    def __repr__(self):
        return f"Partial Member member_id={self.id}, name={self.name}"

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.id)


class Artist(PartialMember):
    """Represents a Weverse Artist that is fetched from the
    :meth:`weverse.WeverseClient.fetch_artists()` method.
    Inherits from :class:`PartialMember`.

    Shares the same attributes and operations with :class:`PartialMember`.

    Attributes
    ----------
    community_id: :class:`int`
        The community ID of the community the artist belongs to.
    artist_profile: :class:`ArtistProfile`
        The :class:`ArtistProfile` object of the artist.
    join_date: :class:`int`
        The epoch time when the artist joined the community.
    """

    __slots__ = ("community_id", "artist_profile", "join_date")

    def __init__(self, data: dict):
        super().__init__(data)
        self.community_id: int = data["communityId"]
        self.artist_profile: ArtistProfile = ArtistProfile(
            data["artistOfficialProfile"]
        )
        self.join_date: int = data["joinedDate"]

    def __repr__(self):
        return f"Artist member_id={self.id}, name={self.name}"


class ArtistProfile:
    """Represents an Official Weverse Artist Profile.

    .. container:: operations

        .. describe:: str(x)

            Returns the official name of the artist.

    Attributes
    ----------
    official_name: :class:`str`
        The official name of the artist.
    official_image_url: :class:`str`
        The URL of the official image of the artist.
    birthday: :class:`int`
        The epoch time of the artist's birthday.
    """

    __slots__ = ("official_name", "official_image_url", "birthday")

    def __init__(self, data: dict):
        self.official_name: str = data["officialName"]
        self.official_image_url: str = data["officialImageUrl"]
        self.birthday: int = data["birthday"]["date"]

    def __repr__(self):
        return f"Artist Profile official_name={self.official_name}"

    def __str__(self):
        return self.official_name


class PostAuthor(PartialMember):
    """Represents a Weverse Post Author that is an attribute belonging to :class:`.post.Post`
    which is fetched from the :meth:`weverse.WeverseClient.fetch_post()` method.
    Inherits from :class:`PartialMember`.

    Shares the same attributes and operations with :class:`PartialMember`.

    Attributes
    ----------
    community_id: :class:`int`
        The community ID of the community the post author belongs to.
    has_joined: :class:`bool`
        Whether the post author has joined the community.
    is_official: :class:`bool`
        Whether the post author is an official Weverse account.
    profile_is_accessible: :class:`bool`
        Whether the profile of the post author is accessible.
    is_my_profile: :class:`bool`
        Whether the post author is yourself.
    artist_profile: :class:`ArtistProfile` | :class:`None`
        The :class:`ArtistProfile` object of the Post Author if it's an Artist.
    """

    __slots__ = (
        "community_id",
        "has_joined",
        "is_official",
        "profile_is_accessible",
        "is_my_profile",
        "artist_profile",
    )

    def __init__(self, data: dict):
        super().__init__(data)
        self.community_id: int = data["communityId"]
        self.has_joined: bool = data["joined"]
        self.is_official: bool = data["hasOfficialMark"]
        self.profile_is_accessible: bool = data["profileSpaceStatus"] == "ACCESSIBLE"
        self.is_my_profile: bool = data["myProfile"]
        self.artist_profile: ArtistProfile | None = (
            ArtistProfile(data["artistOfficialProfile"])
            if "artistOfficialProfile" in data
            else None
        )

    def __repr__(self):
        return f"Post Author member_id={self.id}, name={self.name}"


class Member(PartialMember):
    """Represents a Weverse Member that is fetched from the
    :meth:`weverse.WeverseClient.fetch_member()` method.
    Inherits from :class:`PartialMember`.

    Shares the same attributes and operations with :class:`PartialMember`.

    Attributes
    ----------
    community_id: :class:`int`
        The community ID of the community the member belongs to.
    profile_cover_image_url: :class:`str` | :class:`None`
        The URL of the profile cover image of the member, if any.
    profile_comment: :class:`str` | :class:`None`
        The profile comment of the member, if any.
    has_joined: :class:`bool`
        Whether the member has joined the community.
    has_membership: :class:`bool`
        Whether the member has a paid membership to the community.
    is_official: :class:`bool`
        Whether the member is an official Weverse account.
    is_hidden: :class:`bool`
        Whether the member is hidden.
    is_blinded: :class:`bool`
        Whether the member is blinded.
    is_followed: :class:`bool`
        Whether the signed-in account is following the member.
    is_my_profile: :class:`bool`
        Whether the member is yourself.
    first_joined_at: :class:`int`
        The time the member first joined the community at, in epoch.
    follow_count: :class:`int` | :class:`None`
        The number of followers the member has, if available.
    artist_profile: :class:`ArtistProfile` | :class:`None`
        The :class:`ArtistProfile` object of the member if it's an Artist.
    """

    __slots__ = (
        "community_id",
        "profile_cover_image_url",
        "profile_comment",
        "has_joined",
        "has_membership",
        "is_official",
        "is_hidden",
        "is_blinded",
        "is_followed",
        "is_my_profile",
        "first_joined_at",
        "follow_count",
        "artist_profile",
    )

    def __init__(self, data: dict):
        super().__init__(data)
        self.community_id: int = data["communityId"]
        self.profile_cover_image_url: str | None = data.get("profileCoverImageUrl")
        self.profile_comment: str | None = data.get("profileComment")
        self.has_joined: bool = data["joined"]
        self.has_membership: bool = data["hasMembership"]
        self.is_official: bool = data["hasOfficialMark"]
        self.is_hidden: bool = data["hidden"]
        self.is_blinded: bool = data["blinded"]
        self.is_followed: bool = data["followed"]
        self.is_my_profile: bool = data["myProfile"]
        self.first_joined_at: int = data["firstJoinAt"]
        self.follow_count: int | None = (
            data["followCount"]["followerCount"] if "followCount" in data else None
        )
        self.artist_profile: ArtistProfile | None = (
            ArtistProfile(data["artistOfficialProfile"])
            if "artistOfficialProfile" in data
            else None
        )

    def __repr__(self):
        return f"Member member_id={self.id}, name={self.name}"
