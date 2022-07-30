<div id="top"></div>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://gisart.herokuapp.com/home">
  <img src="https://github.com/berlin-experiment/readme-files/blob/master/imgs/gisart-blog-site/Main%20Desktop.png?raw=true" alt="Mock Up Design of Product"></a>
</div>
  
  

  <h3 align="center">GISart</h3>

  <p align="center">
    SEO_01 Assessment Spring Semster 2022 for
    <br />
    <a href="https://code.berlin/en/"><strong>CODE University of Applied Sciences</strong></a>
    <br />
    <br />
    <a href="https://gisart.herokuapp.com">View Demo</a>
    ·
    <a href="https://github.com/berlin-experiment/GISart_Blog/issues">Report Bug</a>
    ·
    <a href="https://github.com/berlin-experiment/GISart_Blog/issues">Request Feature</a>
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
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

A Flask visual blog application for users to upload and share satellite, remote sensing, or cartographic photos on this website. The <a href="https://unsplash.com/@usgs"><strong>USGS</strong></a>'s photographic posts on Unsplash served as the site's primary source of <a href="https://unsplash.com/s/photos/satellite-imagery"><strong> inspiration</strong></a>. 

A geographic information system is a type of database that combines software tools for managing, analysing, and displaying geographic data with the database itself. GIS connects data to a map and combines all kinds of descriptive data with location data. This offers a basis for mapping and analysis, which are applied in science and practically every sector of the economy. These visualisations can be artistic as well as analytical and functional. Utilize the GIS tools and your creativity or curiosity to change the way we can see the world and share the results on the GISart site.

Alternatively, fork this repo and create a visual blog site of your own.

<div align="center">
  <img src="https://github.com/berlin-experiment/readme-files/blob/master/imgs/gisart-blog-site/Tab%20One.png?raw=true" alt="Mock Up Design of Product" width="508">
</div>

This App Includes:

* Basic frontend structure,
* Dynamic views for Unauthenticated & authenticated sessions with session based routing,
* Sign up, login, logout, and delete account feature,
* Secure sessions that allow users to post to profile & update personal content,
* PostgresSQL Database intergration for CRUD operations which allows users to post unique content,
* AWS S3 Intergration
* Allow users to store & display user generated content,
* Content-type (image) & size restrictions,
* Enforces unique content for username & post titles, and
* Aesthetically pleasing responsive Space themed CSS.


<div align="center">
  <img src="https://github.com/berlin-experiment/readme-files/blob/master/imgs/gisart-blog-site/Tab%20five.png?raw=true" alt="Mock Up Design of Product" width="508">
</div>

Keep in mind there are some limitations and issues with this application. As is user image content and passwords cannot be updated once posted and a user must delete all there posts before deleting there account - I am working on adding this functionality.

NOTE: All undredit images in this repo are images I created myself with the use of <a href="https://www.sentinel-hub.com">Sentinel Hub</a>

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap 5" width="100">
* <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" width="100">
* <img src="https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white" alt="Heroku" width="100">
* <img src="https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" alt="AWS" width="100">
* <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" width="100">

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* <a href="https://www.python.org/downloads/">Python 3.10 +</a>

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/berlin-experiment/GISart_Blog.git
   ```
2. To create a virtual environment in Python, navigate to your project directory in the terminal
   ```sh
   python3 -m venv venv
   ```
3. Activate your venv
   On macOS and Linux run:
   ```sh
   source venv/bin/activate
   ```
   On Windows run: 
   ```sh
   venv\Scripts\activate.bat
   ```
4. Install PIP packages
   ```sh
   pip install requirements.txt
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make GISart better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See <a href="https://opensource.org/licenses/MIT">Opensource.org</a> for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Stacey Kenny - <a href="https://twitter.com/berlinXperiment">@berlinXperiment</a> - <a href="mailto:stacey.kenny@code.berlin">stacey.kenny@code.berlin</a>

Project Link: <a href="https://github.com/berlin-experiment/GISart_Blog">berlin-experiment/GISart_Blog</a>

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Here are all of the resources I found useful:

* <a href="https://flask.palletsprojects.com/en/2.1.x/">Flask</a>
* <a href="https://www.youtube.com/watch?v=0Qxtt4veJIc">Codemy.com</a>
* <a href="https://www.youtube.com/watch?v=6WruncSoCdI">Julian Nash</a>
* <a href="https://stackoverflow.com/questions/46430061/flask-database-migrations-on-heroku">Stackoverflow</a>

<p align="right">(<a href="#top">back to top</a>)</p>
