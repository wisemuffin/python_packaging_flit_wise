from unittest.mock import patch
import pytest
import python_packaging_flit_wise


def test_get():
    with patch("python_packaging_flit_wise.http.get") as mock:
        mock.return_value = {
            "resultCount": 1,
            "results": [
                {
                    "wrapperType": "track",
                    "kind": "podcast",
                    "collectionId": 979020229,
                    "artistName": "Michael Kennedy (@mkennedy)",
                    "collectionName": "Talk Python To Me",
                    "collectionViewUrl": "https://podcasts.apple.com/us/podcast/id979020229?uo=4",
                    "feedUrl": "https://talkpython.fm/episodes/rss",
                    "primaryGenreName": "Technology",
                    "artworkUrl600": "https://whatever/image/979020229.png",
                    "trackCount": 26,
                    "country": "USA",
                }
            ],
        }

        podcast = python_packaging_flit_wise.get(979020229)
        assert isinstance(podcast, python_packaging_flit_wise.Podcast)
        assert podcast.id == 979020229
        assert podcast.name == "Talk Python To Me"
        assert podcast.author == "Michael Kennedy (@mkennedy)"
        assert podcast.url == "https://podcasts.apple.com/us/podcast/id979020229"
        assert podcast.feed == "https://talkpython.fm/episodes/rss"
        assert podcast.category == "Technology"
        assert podcast.image == "https://whatever/image/979020229.png"
        assert podcast.country == "USA"
        assert podcast.episode_count == 26


def test_invalid_kind():
    with patch("python_packaging_flit_wise.http.get") as mock:
        mock.return_value = {
            "resultCount": 1,
            "results": [
                {
                    "kind": "ebook",
                    "trackId": 1435797751,
                    "trackName": "Python Programming For Beginners",
                }
            ],
        }
        podcast = python_packaging_flit_wise.get(1435797751)
        assert podcast is None


def test_nothing_found():
    with patch("python_packaging_flit_wise.http.get") as mock:
        mock.return_value = {"resultCount": 0, "results": []}
        podcast = python_packaging_flit_wise.get(979020229)
        assert podcast is None


def test_failed():
    with patch("python_packaging_flit_wise.http.get") as mock:
        mock.side_effect = Exception()
        with pytest.raises(Exception):
            python_packaging_flit_wise.get(979020229)