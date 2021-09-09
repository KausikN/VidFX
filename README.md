# VidFX
 A python tool (UI and Code) for editing videos and adding fun effects to webcam and video

# GUI
[![https://infinityjoker-apps.herokuapp.com/](https://pyheroku-badge.herokuapp.com/?app=infinityjoker-apps&style=plastic)](https://infinityjoker-apps.herokuapp.com/)

 - GUI built using streamlit
 - To use app locally,
    - Clone the repo and run [StartUI.sh](StartUI.sh) to view the app on your browser!
 - App is also hosted remotely on heroku using my common host app,
    - [https://infinityjoker-apps.herokuapp.com/](https://infinityjoker-apps.herokuapp.com/)

    - In the Common Host App, simply choose a project to load and click load and deploy.

    - Then go ahead and use the app! :)

    - If you want to change to another app, simply click on View Other Projects in top left and choose any other project and load and deploy.

# UI Effects Visualiser
  [![Generic badge](https://img.shields.io/badge/Effects-List-<COLOR>.svg)](EffectsLibrary/Effects.txt)
   
  View/Save effects easily for webcam or any video

  CommonEffects:
     
    Effects that are applied to Input Video before applying further effects

  EffectFuncs:

    - Effects applied for video to display

    - Multiple effect sequences are separated by a ',' line

    - Set of Sequences of effects are applied and all of them are appended as a single frame for an input frame from the video

  For full list of effects with their parameters see [Effect List](EffectsLibrary/Effects.txt)

  ![UI Output Image](DocImages/UIOutput.PNG)

# Features

   - Add same effects for images

     ![Effect Image](GeneratedVisualisations/Effects/Effect_CannyEdges.jpg)
   
   - Effects can also be used in combination with each other (BinValues + Blur)

     ![Combined Effects Video Image](GeneratedVisualisations/EffectCombination_1.gif)

   - Multiple Effects can be viewed at same time

     ![Multiple Effects Video Image](GeneratedVisualisations/MultipleEffects_1.gif)
  
   - Effects Transistion can be applied to an image to form a video of the image under an effect with varying parameters (Decreasing Scale and Increasing Rotation)

     ![EffectsTransistion Video](GeneratedVisualisations/Effects/EffectTransistion_GeometricTransform.gif)

# Effects

   - None

     ![None Effect](GeneratedVisualisations/Effects/Effect_None.jpg)

   - Binarise

     ![Binarise Effect](GeneratedVisualisations/Effects/Effect_Binarise.jpg)

   - GreyScale

     ![GreyScale Effect](GeneratedVisualisations/Effects/Effect_GreyScale.jpg)

   - RGB2BGR

     ![RGB2BGR Effect](GeneratedVisualisations/Effects/Effect_RGB2BGR.jpg)

   - RedChannel

     ![RedChannel Effect](GeneratedVisualisations/Effects/Effect_RedChannel.jpg)

   - BlueChannel

     ![BlueChannel Effect](GeneratedVisualisations/Effects/Effect_BlueChannel.jpg)

   - GreenChannel

     ![GreenChannel Effect](GeneratedVisualisations/Effects/Effect_GreenChannel.jpg)

   - MostDominantColor

     ![MostDominantColor Effect](GeneratedVisualisations/Effects/Effect_MostDominantColor.jpg)

   - LeastDominantColor

     ![LeastDominantColor Effect](GeneratedVisualisations/Effects/Effect_LeastDominantColor.jpg)

   - ScaleValues

     ![ScaleValues Effect](GeneratedVisualisations/Effects/Effect_ScaleValues.jpg)

   - ClipValues

     ![ClipValues Effect](GeneratedVisualisations/Effects/Effect_ClipValues.jpg)

   - BinValues

     ![BinValues Effect](GeneratedVisualisations/Effects/Effect_BinValues.jpg)

   - ResizeBlur

     ![ResizeBlur Effect](GeneratedVisualisations/Effects/Effect_ResizeBlur.jpg)

   - AddFrame

     ![AddFrame Effect](GeneratedVisualisations/Effects/Effect_AddFrame.jpg)

   - GaussianNoise

     ![GaussianNoise Effect](GeneratedVisualisations/Effects/Effect_GaussianNoise.jpg)

   - SpeckleNoise

     ![SpeckleNoise Effect](GeneratedVisualisations/Effects/Effect_SpeckleNoise.jpg)

   - SaltPepperNoise

     ![SaltPepperNoise Effect](GeneratedVisualisations/Effects/Effect_SaltPepperNoise.jpg)

   - SemanticSegmentation

     ![SemanticSegmentation Effect](GeneratedVisualisations/Effects/Effect_SemanticSegmentation.jpg)

   - InstanceSegmentation

     ![InstanceSegmentation Effect](GeneratedVisualisations/Effects/Effect_InstanceSegmentation.jpg)

   - CannyEdges

     ![CannyEdges Effect](GeneratedVisualisations/Effects/Effect_CannyEdges.jpg)

   - ValueCount Plot

     ![ValueCount Effect](GeneratedVisualisations/Effects/Effect_ValueCount.jpg)

   - FrameDelay

     ![FrameDelay Effect](GeneratedVisualisations/Effects/Effect_FrameDelay.gif)

   - And many more! :O
   
     For full list of effects with their parameters see [Effect List](EffectsLibrary/Effects.txt).