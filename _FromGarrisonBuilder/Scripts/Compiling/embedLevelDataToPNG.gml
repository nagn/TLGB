MapEntityCheck();
  
  var target_PNG, c, loadWM, loadBGs;
  
  c = 0;
  if (global.quickSave == 0)
  {
        target_PNG = get_open_filename("PNG|*.png","")
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
  //if(mc.compressedWalkmaskString == "")
    mc.compressedWalkmaskString = compressWalkmaskToString();
  
  // get entity data and compressed walkmask data, and put them together
  var leveldata;
  leveldata = writeEntitiesToString() + chr(10) + mc.compressedWalkmaskString;
  
  GG2DLL_embed_PNG_leveldata(target_PNG, leveldata);
