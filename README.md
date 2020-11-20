# LocalRenderFarm
Blender Add-on to create a local render farm.

## Steps to use:
1. Download the [server add-on](https://github.com/HuangPatrick16777216/LocalRenderFarm/releases/download/v0.1.0/local_render_farm_server.zip) on the server computer, and the [client add-on](https://github.com/HuangPatrick16777216/LocalRenderFarm/releases/download/v0.1.0/local_render_farm_client.zip) on all client computers.
    * Note: In this version (0.1.0), rendering on the server computer is not possible, so please assign a weaker computer as the server.
2. Install the downloaded add-on on all computers. The UI can be found in *Properties >> Render >> Local Render Farm*
3. Activate the server by clicking on the *Start Server* button.
4. Connect all clients by typing in the server IP and clicking *Connect*.
5. Make sure all clients have JPEG set as the output paramter.
6. Set the output directory on the server, and start the render.

## Notes:
* This add-on uses *threading*, or executing multiple programs at once. This may leave a program running even after Blender is closed. To stop the program, open the task manager and end all tasks called "Blender".
* Please do not try to use this add-on without following the steps exactly, because it may mess up your files.