#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Any

class ContentGenerator:
    """
    Class to generate NFO and BBCode content from media metadata.
    """

    def __init__(self, media_info: Dict[str, Any], analyzer: ContentAnalyzer):
        """
        Initialize the ContentGenerator.
        
        :param media_info: Dict[str, Any] - Media information extracted by MediaInfo
        :param analyzer: ContentAnalyzer - Content analyzer with title, year, and type information
        """
        self.media_info = media_info
        self.analyzer = analyzer

    def generate_torrent_title(self) -> str:
        """
        Generate the torrent file title according to standards.
        
        :return: str - Formatted torrent title
        """
        if self.analyzer.content_type == "serie":
            return (f"{self.analyzer.title} ({self.analyzer.year_range}) - Intégrale - "
                    f"{self.media_info.get('language_tag', '')} - {self.media_info.get('source', '')} - "
                    f"{self.media_info.get('resolution', '')} - {self.media_info.get('video_codec', '').split(' ')[0]}")
        else:  # Film
            return (f"{self.analyzer.title} ({self.analyzer.year}) - "
                    f"{self.media_info.get('language_tag', '')} - {self.media_info.get('source', '')} - "
                    f"{self.media_info.get('resolution', '')} - {self.media_info.get('video_codec', '').split(' ')[0]}")

    def generate_nfo_content(self) -> str:
        """
        Generate NFO file content.
        
        :return: str - Formatted NFO content
        """
        if self.analyzer.content_type == "serie":
            return self._generate_serie_nfo()
        else:
            return self._generate_film_nfo()

    def _generate_serie_nfo(self) -> str:
        """
        Generate NFO content for a TV series.
        
        :return: str - Formatted NFO content for a series
        """
        title = self.analyzer.title
        year_range = self.analyzer.year_range
        
        # Format bitrate and duration if available
        bitrate = "?"
        if self.media_info.get('overall_bitrate', '0').isdigit():
            bitrate = str(int(int(self.media_info.get('overall_bitrate', '0')) / 1000))
            
        duration = "?"
        if self.media_info.get('duration', '0').replace('.', '', 1).isdigit():
            duration = str(int(float(self.media_info.get('duration', '0')) / 60))
        
        return f"""░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░ {title.upper()} ({year_range}) ░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

▓ INFORMATIONS GÉNÉRALES
 ▪ Titre.............: {title}
 ▪ Année.............: {year_range}
 ▪ Genres............: À compléter
 ▪ Créateurs.........: À compléter
 ▪ Acteurs principaux.: À compléter
 ▪ Saisons...........: {self.analyzer.season_count} saison{'s' if self.analyzer.season_count > 1 else ''} ({self.analyzer.episode_count} épisode{'s' if self.analyzer.episode_count > 1 else ''})
 ▪ Langue............: {self.media_info.get('language_tag', 'Unknown')}

▓ INFORMATIONS TECHNIQUES
 ▪ Format............: {self.media_info.get('format', 'Unknown')}
 ▪ Durée moyenne.....: ~{duration} minutes par épisode
 ▪ Source............: {self.media_info.get('source', 'Unknown')}
 ▪ Résolution........: {self.media_info.get('resolution', 'Unknown')} ({self.media_info.get('width', 'Unknown')}x{self.media_info.get('height', 'Unknown')})
 ▪ Codec Vidéo.......: {self.media_info.get('video_codec', 'Unknown')}
 ▪ Bitrate Vidéo.....: ~{bitrate} kb/s
 ▪ Codec Audio.......: {', '.join(self.media_info.get('audio_codecs', ['Unknown']))}
 ▪ Sous-titres.......: {', '.join(self.media_info.get('subtitle_languages', ['None']))}

▓ SYNOPSIS
À compléter

▓ INFORMATIONS COMPLÉMENTAIRES
Ce torrent contient l'intégrale de la série {title}, de la saison 1 à la saison {self.analyzer.season_count}, en version {self.media_info.get('language_tag', '')}. Chaque épisode est accompagné de son fichier NFO détaillé et d'une miniature.

░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░"""

    def _generate_film_nfo(self) -> str:
        """
        Generate NFO content for a movie.
        
        :return: str - Formatted NFO content for a movie
        """
        title = self.analyzer.title
        year = self.analyzer.year
        
        # Format bitrate and duration if available
        bitrate = "?"
        if self.media_info.get('overall_bitrate', '0').isdigit():
            bitrate = str(int(int(self.media_info.get('overall_bitrate', '0')) / 1000))
            
        duration = "?"
        if self.media_info.get('duration', '0').replace('.', '', 1).isdigit():
            duration = str(int(float(self.media_info.get('duration', '0')) / 60))
        
        return f"""░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░ {title.upper()} ({year}) ░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

▓ INFORMATIONS GÉNÉRALES
 ▪ Titre.............: {title}
 ▪ Année.............: {year}
 ▪ Genres............: À compléter
 ▪ Réalisateur.......: À compléter
 ▪ Acteurs principaux.: À compléter
 ▪ Langue............: {self.media_info.get('language_tag', 'Unknown')}

▓ INFORMATIONS TECHNIQUES
 ▪ Format............: {self.media_info.get('format', 'Unknown')}
 ▪ Durée.............: {duration} minutes
 ▪ Source............: {self.media_info.get('source', 'Unknown')}
 ▪ Résolution........: {self.media_info.get('resolution', 'Unknown')} ({self.media_info.get('width', 'Unknown')}x{self.media_info.get('height', 'Unknown')})
 ▪ Codec Vidéo.......: {self.media_info.get('video_codec', 'Unknown')}
 ▪ Bitrate Vidéo.....: ~{bitrate} kb/s
 ▪ Codec Audio.......: {', '.join(self.media_info.get('audio_codecs', ['Unknown']))}
 ▪ Sous-titres.......: {', '.join(self.media_info.get('subtitle_languages', ['None']))}

▓ SYNOPSIS
À compléter

░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░"""

    def generate_bbcode_content(self) -> str:
        """
        Generate BBCode content for forum posting.
        
        :return: str - Formatted BBCode content
        """
        if self.analyzer.content_type == "serie":
            return self._generate_serie_bbcode()
        else:
            return self._generate_film_bbcode()

    def _generate_serie_bbcode(self) -> str:
        """
        Generate BBCode content for a TV series.
        
        :return: str - Formatted BBCode content for a series
        """
        title = self.analyzer.title
        year_range = self.analyzer.year_range
        
        # Create torrent title according to rules
        torrent_title = self.generate_torrent_title()
        
        # Format bitrate and duration if available
        bitrate = "?"
        if self.media_info.get('overall_bitrate', '0').isdigit():
            bitrate = str(int(int(self.media_info.get('overall_bitrate', '0')) / 1000))
            
        duration = "?"
        if self.media_info.get('duration', '0').replace('.', '', 1).isdigit():
            duration = str(int(float(self.media_info.get('duration', '0')) / 60))
        
        return f"""[center][img=600x800]https://URL_DE_VOTRE_IMAGE/poster.jpg[/img][/center]

[center][size=18][b]{torrent_title}[/b][/size][/center]

[b]Créateurs:[/b] À compléter
[b]Acteurs principaux:[/b] À compléter
[b]Genre:[/b] À compléter
[b]Année de sortie:[/b] {year_range}

[b]Résumé:[/b]
À compléter

[b]Informations sur l'upload:[/b]
[list]
[*]Format: {self.media_info.get('format', 'Unknown')}
[*]Langues: {self.media_info.get('language_tag', 'Unknown')} ({', '.join(self.media_info.get('audio_languages', ['Unknown']))})
[*]Source: {self.media_info.get('source', 'Unknown')}
[*]Résolution: {self.media_info.get('resolution', 'Unknown')} ({self.media_info.get('width', 'Unknown')}x{self.media_info.get('height', 'Unknown')})
[*]Codec vidéo: {self.media_info.get('video_codec', 'Unknown')}
[*]Bitrate vidéo: ~{bitrate} kb/s
[*]Codec audio: {', '.join(self.media_info.get('audio_codecs', ['Unknown']))}
[*]Sous-titres: {', '.join(self.media_info.get('subtitle_languages', ['None']))}
[*]Nombre d'épisodes: {self.analyzer.episode_count}
[*]Nombre de saisons: {self.analyzer.season_count}
[/list]

[center][img=700x175]https://URL_DE_VOTRE_IMAGE/banner.jpg[/img][/center]

[center][img]https://URL_DE_VOTRE_IMAGE/fanart.jpg[/img][/center]"""

    def _generate_film_bbcode(self) -> str:
        """
        Generate BBCode content for a movie.
        
        :return: str - Formatted BBCode content for a movie
        """
        title = self.analyzer.title
        year = self.analyzer.year
        
        # Create torrent title according to rules
        torrent_title = self.generate_torrent_title()
        
        # Format bitrate and duration if available
        bitrate = "?"
        if self.media_info.get('overall_bitrate', '0').isdigit():
            bitrate = str(int(int(self.media_info.get('overall_bitrate', '0')) / 1000))
            
        duration = "?"
        if self.media_info.get('duration', '0').replace('.', '', 1).isdigit():
            duration = str(int(float(self.media_info.get('duration', '0')) / 60))
        
        return f"""[center][img=600x800]https://URL_DE_VOTRE_IMAGE/poster.jpg[/img][/center]

[center][size=18][b]{torrent_title}[/b][/size][/center]

[b]Réalisateur:[/b] À compléter
[b]Acteurs principaux:[/b] À compléter
[b]Genre:[/b] À compléter
[b]Année de sortie:[/b] {year}

[b]Résumé:[/b]
À compléter

[b]Informations sur l'upload:[/b]
[list]
[*]Format: {self.media_info.get('format', 'Unknown')}
[*]Langues: {self.media_info.get('language_tag', 'Unknown')} ({', '.join(self.media_info.get('audio_languages', ['Unknown']))})
[*]Source: {self.media_info.get('source', 'Unknown')}
[*]Résolution: {self.media_info.get('resolution', 'Unknown')} ({self.media_info.get('width', 'Unknown')}x{self.media_info.get('height', 'Unknown')})
[*]Codec vidéo: {self.media_info.get('video_codec', 'Unknown')}
[*]Bitrate vidéo: ~{bitrate} kb/s
[*]Codec audio: {', '.join(self.media_info.get('audio_codecs', ['Unknown']))}
[*]Sous-titres: {', '.join(self.media_info.get('subtitle_languages', ['None']))}
[*]Durée: {duration} minutes
[/list]

[center][img]https://URL_DE_VOTRE_IMAGE/fanart.jpg[/img][/center]"""


