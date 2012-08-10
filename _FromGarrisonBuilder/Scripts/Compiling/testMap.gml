MapEntityCheck();

  var target_PNG, c, loadWM, loadBGs;
  
  c = 0;
  if (global.quickSave == 0)
  {
        target_PNG = get_open_filename("PNG|*.png","");
        if (target_PNG == "")
        {
            break;
        }
  }
  else
  {
        target_PNG = global.rawBG;
        if (target_PNG == "")
        {
            target_PNG = global.rawWM;
        }
        if (target_PNG == "")
        {
              show_message("Autosave Failed.");  
              break;
        }
  }
  
  // if we haven't done so already, compress the walkmask to a string
  if(mc.compressedWalkmaskString == "")
    mc.compressedWalkmaskString = compressWalkmaskToString();
  
  // get entity data and compressed walkmask data, and put them together
  var leveldata;
  leveldata = writeEntitiesToString() + chr(10) + mc.compressedWalkmaskString;
  
  GG2DLL_embed_PNG_leveldata(target_PNG, leveldata);
  
  if (!(directory_exists(program_directory + "\Maps\")))
  {
    directory_create(program_directory + "\Maps\");
  }
  
  // let's make a copy of this map in the maps folder.
  if (global.bgName == "") && (global.wkmskName != "")
  {
        if (file_exists("Maps\" + global.wkmskName + ".png"))
        {
            file_delete("Maps\" + global.wkmskName + ".png");
        }
        file_copy(target_PNG, "Maps\" + global.wksmkName + ".png"); // let's make a copy of this map in the maps folder.
        loadWM = true;
        loadBGs = false;
  }
  else if (global.bgName != "") && (global.wkmskName == "")
  {
        if (file_exists("Maps\" + global.bgName + ".png"))
        {
            file_delete("Maps\" + global.bgName + ".png");
        }
        file_copy(target_PNG, "Maps\" + global.bgName + ".png"); // let's make a copy of this map in the maps folder.
        loadWM = false;
        loadBGs = true;
  }
  else if (global.bgName != "") && (global.wkmskName != "")
  {
        if (file_exists("Maps\" + global.bgName + ".png"))
        {
            file_delete("Maps\" + global.bgName + ".png");
        }
        file_copy(target_PNG, "Maps\" + global.bgName + ".png"); // let's make a copy of this map in the maps folder.
        loadWM = false;
        loadBGs = true;
  }
  
  // let's begin testing.
  if (loadWM == true) && (loadBGs == false)
  {
        execute_program(chr(34) + global.gg2Dir + "\Gang Garrison 2.exe" + chr(34), "-map" + " " + global.wkmskName, false); 
  }
  else if (loadBGs == true) && (loadWM == false)
  {
        execute_program(chr(34) + global.gg2Dir + "\Gang Garrison 2.exe" + chr(34), "-map" + " " + global.bgName, false);
  }
