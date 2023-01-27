# Minecraft World Generator

This script can generate worlds using a default Craftbukkit/Spigot/Paper Server and the
plugin [Fast Chunk Pregenerator](https://www.spigotmc.org/resources/fast-chunk-pregenerator.74429/).

It works by copying the template in the server-directory, running the server, executing the generation command for FCP,
stopping the server and finally copying the world directory.

## Setup

- Put a Paper-JAR named `server.jar` into the `server` folder
- Download FCP and put the plugin into `server/plugins`
- Create the `eula.txt` and `server.properties` inside the `server`directory, so that you can startup the server without
  any interaction (and you have to accept the EULA beforehand)
- Change the last lines inside of `main.py` to represent the worlds you want to pregenerate
- Install the requirements from `requirements.txt`
- Run the `main.py`

You should see the minecraft server starting and generating a world. Afterwards you can find the generated worlds inside
the `output` directory.