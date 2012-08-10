/*
Deleting out the checks out of Testmap and embedLevelDataToPNG saves 188 lines of code
And its cleaner now.
*/

strayEntityFix();

  // preliminary check to see if the user placed the correct entities or the correct combination of entities.
  var neutralIntelExists, neutralIntelSpawnExists, capsExist, cap1Exist, cap2Exist, cap3Exist, cap4Exist, cap5Exist, bluIntelSpawnExists, redIntelSpawnExists, bluIntelExists, redIntelExists, sufficientCapMats, ArenacpExist, GenBlueExist, GenRedExist, KothcpExist;
  neutralIntelExists = false;
  neutralIntelSpawnExists = false;
  bluIntelSpawnExists = false;
  redIntelSpawnExists = false;
  bluIntelExists = false;
  redIntelExists = false;
  sufficientCapMats = false;
  cap1Exist = false;
  cap2Exist = false;
  cap3Exist = false;
  cap4Exist = false;
  cap5Exist = false;
  capsExist = false;
  ArenacpExist = false;
  GenRedExist = false;
  GenBlueExist = false;
  KothcpExist = false
  with (LevelEntity)
  {
    if (type == "NeutralIntel")
    {
        neutralIntelExists = true;
    }
    else if (type == "redintel")
    {
        redIntelExists = true;
    }
    else if (type == "blueintel")
    {
        bluIntelExists = true;
    }
    else if (type == "IntelSpawn")
    {    
         neutralIntelSpawnExists = true;
    }
    else if (type == "RedIntelSpawn")
    {    
         redIntelSpawnExists = true;
    }
    else if (type == "BlueIntelSpawn")
    {    
         bluIntelSpawnExists = true;
    }
    else if (type == "ArenaControlPoint")
    {    
    if instance_number(ArenaControlPoint)>1 {
            show_message("Only one Control Point possible!")
            exit; }
         ArenacpExist = true;
    }
    else if (type == "KothControlPoint")
    {    
    if instance_number(KothControlPoint)>1 {
            show_message("Only one Control Point possible!")
            exit; }
         KothcpExist = true;
    }
      else if (type == "GeneratorRed")
    {    
         GenRedExist = true;
        if instance_number(GeneratorRed)>1 {
            show_message("Only one Generator for each team. No Unbalancing for you whore.")
            exit; 
            }
    }
      else if (type == "GeneratorBlue")
    {    
         GenBlueExist = true;
         if instance_number(GeneratorBlue)>1 {
            show_message("Only one Generator for each team. No Unbalancing for you whore.")
            exit;
            }
    }
    else if (type == "CapturePoint")
    {  
        sufficientCapMats = true;
    }
    else if (global.gamemode == 2) {
     if (type == "controlPoint1")
    {
        if (cap1Exist == true)
        {
            show_message("Please do not place more than one instance of a unique control point.");
            exit;
        }
        else
        {
            cap1Exist = true;
        }
    }
    else if (type == "controlPoint2")
    {
        if (cap2Exist == true)
        {
            show_message("Please do not place more than one instance of a unique control point.");
            exit;
        }
        else
        {
            cap2Exist = true;
        }       
    }
    else if (type == "controlPoint3")
    {
        if (cap3Exist == true)
        {
            show_message("Please do not place more than one instance of a unique control point.");
            exit;
        }
        else
        {
            cap3Exist = true;
        }
    }
    else if (type == "controlPoint4")
    {
        if (cap4Exist == true)
        {
            show_message("Please do not place more than one instance of a unique control point.");
            exit;
        }
        else
        {
            cap4Exist = true;
        }
    }
    else if (type == "controlPoint5")
    {
        if (cap5Exist == true)
        {
            show_message("Please do not place more than one instance of a unique control point.");
            exit;
        }
        else
        {
            cap5Exist = true;
        }
    }
  }
}
  
  if (cap1Exist == true || cap2Exist == true || cap3Exist == true || cap4Exist == true || cap5Exist == true)
  {
      capsExist = true;
  }
  // Traditional CTF check
  if global.gamemode == 1 {
    if (((redIntelExists == true) && (bluIntelExists == false)) || ((redIntelExists == false) && (bluIntelExists == true)) || ((redIntelExists == false) && (bluIntelExists == false))) {
        show_message("If you are making a traditional CTF map, you must place both the Red intelligence and the Blu intelligence somewhere on the map.");
        exit;
    }
  }
  else if global.gamemode == 5 {
        if (GenRedExist = false && GenBlueExist = true) || (GenRedExist = true && GenBlueExist = false)
        {
  // Generators.
        show_message("For generator maps you need both generators.");
        exit;
        }
  }
  else if global.gamemode == 4 {
        if (ArenacpExist == false || sufficientCapMats == false) 
        {
    // For the Arena maps.
    show_message("Please make sure you've placed the arena capture point AND the Capture Zones.");
    exit;
        }
    }
    else if global.gamemode == 7 {
        if (KothcpExist == false  || sufficientCapMats == false) 
        {
    // For the Koth maps.
    show_message("Please make sure you've placed the Koth capture point AND the Capture Zones.");
    exit;
        }
  }
  else if global.gamemode == 2 {
  if (capsExist == true && sufficientCapMats == false || capsExist == false && sufficientCapMats == true) 
  {
    // For the CP maps.
    show_message("Please make sure you've placed all the Capture Points AND Capture Zones.");
    exit;
  }  
  else if global.gamemode == 3 {
    if (instance_number(NextAreaO_ent)<2 && (instance_number(controlPoint1_ent) != 3) && (instance_number(controlPoint2_ent) !=3)) {
        show_message("Please make sure you've placed the both NextArea entitys,#AND 3 CPs of both types.")
        exit;
        }
 
 /* global.totalMapAreas = 1+instance_number(NextAreaO);

        if global.totalMapAreas > 1 {
            global.area[1] = 0;
    
            for(i=2;i<=global.totalMapAreas;i+=1) {
            global.area[i] = instance_find(NextAreaO,i-2).y; 
        }
        }*/ 
        }
}
