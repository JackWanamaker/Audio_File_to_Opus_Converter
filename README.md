<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Unlicense][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/JackWanamaker/Audio_File_To_Opus_Converter">
    <img src="https://i.imgur.com/8T7ip83.jpeg" alt="Logo" width="320" height="240">
  </a>

<h3 align="center">Audio File To Opus Automatic Converter</h3>

  <p align="center">
    Helps automatically convert a library of music to Opus format
    <br />
    <a href="https://github.com/JackWanamaker/Audio_File_To_Opus_Converter"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/JackWanamaker/Audio_File_To_Opus_Converter/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/JackWanamaker/Audio_File_To_Opus_Converter/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Video Title](https://i.imgur.com/rlq5OYh.png)](https://www.youtube.com/watch?v=HGC0RAhUWWo)


This project is built to automatically convert your lossless audio albums to Opus with no hassle! Perfect for people who want to build their own music libraries, but are tired of sacrificing space, sound quality, and time.



### Built With

* [![Python][Python.org]][Python-url]



<!-- GETTING STARTED -->
## Getting Started

Please follow the instructions below, and/or follow along with the video guide above.

### Prerequisites

1. This must be run on a Windows Operating System
2. Download the latest version of [Python](https://www.python.org/downloads/), latest version of [FFmpeg](https://ffmpeg.org/download.html), and latest version of [TagEditor](https://github.com/Martchus/tageditor).
3. Install all of the above and set them as [Path Variables](https://youtu.be/gb9e3m98avk?si=Rnv1_87uFZ6Lbui0)
4. Install the mutagen Python library by opening command prompt or terminal and type `pip install mutagen`. 

### Installation

1. Download my entire repo and extract it to a location that you will remember and is convenient
2. Open a file explorer window and navigate to your music folder.
3. Create 4 folders within your music folder: UNPROCESSED, TEMP, ARCHIVE, and COMPRESSED. It should be this type of structure:

<br><br>

![Example Folder Structure](https://i.imgur.com/RlB4xMN.png)

4. Open `main.py` in an IDE or text editor
5. Set MAIN_PATH, FLAC_FOLDER, OPUS_FOLDER, SYNC_FOLDER, and TEMP_FOLDER as C:/Users/MyUser/Music (or location of your music folder), ARCHIVE, COMPRESSED, UNPROCESSED, and TEMP. Here is an example:

<br>

```
MAIN_PATH = r"C:\Users\MyUser\Music"
FLAC_FOLDER = r"ARCHIVE"
OPUS_FOLDER = r"COMPRESSED"
SYNC_FOLDER = "UNPROCESSED"
TEMP_FOLDER = "TEMP"
```

<br>

6. Set the location of the json and log files for the JSON_PATH and LOG_PATH variables. Here is an example if you put my repo in your documents:

<br>

```
JSON_PATH = r"C:\Users\MyUser\Documents\Audio_File_to_Opus_Converter\data.json"
LOG_PATH = r"C:\Users\MyUser\Documents\Audio_File_to_Opus_Converter\log.txt"
```

<br>

7. (Optional) To have the program run automatically on startup, hit ⊞ + R at the same time to open run, and type `shell:startup` before pressing OK
8. (Optional) Create a batch script with these contents changed to match the location of your Python install and my repo:

<br>

```
@echo off
start "" "PATH_TO_PYTHON_INSTALL" "PATH_TO_MAIN_PYTHON_FILE"
```

<!-- USAGE EXAMPLES -->
## Usage

To get the most out of the automatice converter, I use [SyncThing](https://syncthing.net/) so I can download albums to my phone, have them synced to my PC, and have my program automatically compress them for me. Afterwards, it sends the newly compressed files to my phone, and deletes the lossless files off, all while saving the lossless files in a separate folder on the PC.


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/JackWanamaker/Audio_File_To_Opus_Converter/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=JackWanamaker/Audio_File_To_Opus_Converter" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the Unlicense. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@bensummer49](https://twitter.com/bensummer49) - bensummer49@gmail.com

Project Link: [https://github.com/JackWanamaker/Audio_File_To_Opus_Converter](https://github.com/JackWanamaker/Audio_File_To_Opus_Converter)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/JackWanamaker/Audio_File_To_Opus_Converter.svg?style=for-the-badge
[license-url]: https://github.com/JackWanamaker/Audio_File_to_Opus_Converter/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/bensummer/
[product-screenshot]: images/screenshot.png
<!-- Shields.io badges. You can a comprehensive list with many more badges at: https://github.com/inttter/md-badges -->
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
[Python.org]: https://img.shields.io/badge/python-3776AB?style=for-the-bade&logo=python&logoColor=green
[Python-url]: https://www.python.org
