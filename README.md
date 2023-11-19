# VidFX
 A python tool (UI and Code) for editing videos and adding fun effects to webcam and video

# GUI
[![https://kausikn-commonhostapp-app-zxfv4q.streamlit.app/](https://static.streamlit.io/badges/streamlit_badge_black_red.svg)](https://kausikn-commonhostapp-app-zxfv4q.streamlit.app/)

 - GUI built using streamlit
 - To use app locally,
    - Clone the repo and run [StartUI.sh](StartUI.sh) to view the app on your browser!
 - App is also hosted remotely on my Common-Host-App,
    - [Heroku](https://infinityjoker-apps.herokuapp.com/)
    - [Streamlit](https://kausikn-commonhostapp-app-zxfv4q.streamlit.app/)
 - To use the app on my Common-Host-App,
    - Choose a project to load and click load and deploy.
    - Then go ahead and use the app! 😃
    - If you want to change to another app, simply click on View Other Projects in top left and choose any other project and load and deploy.

# UI Effects Visualiser
  [![Generic badge](https://img.shields.io/badge/Effects-List-<COLOR>.svg)](StreamLitGUI/Effects.txt)
   
  View/Save effects easily for webcam or any video

  Effect Tree:
     
    Various effect nodes can be applied to the input frame from the video or image in a tree structure. Further we can view the effect images at various nodes of the tree in a grid format.

  For full list of effects with their parameters see [Effect List](StreamLitGUI/Effects.txt)

# Features

   - Add same effects for images

     ![Effect Image](Data/GeneratedVisualisations/Effects/Effect_CannyEdges.jpg)
   
   - Effects can also be used in combination with each other (BinValues + Blur)

     ![Combined Effects Video Image](Data/GeneratedVisualisations/EffectCombination_1.gif)

   - Multiple Effects can be viewed at same time in a grid format

     ![Multiple Effects Video Image](Data/GeneratedVisualisations/MultipleEffects_1.gif)
  
   - Effects Transistion can be applied to an image to form a video of the image under an effect with varying parameters (This example is obtained by decreasing scale and increasing rotation parameters in GeometricTransform effect)

     ![EffectsTransistion Video](Data/GeneratedVisualisations/Effects/EffectTransistion_GeometricTransform.gif)

# Effects

   - None

     ![None Effect](Data/GeneratedVisualisations/Effects/Effect_None.jpg)

   - Binarise

     ![Binarise Effect](Data/GeneratedVisualisations/Effects/Effect_Binarise.jpg)

   - GreyScale

     ![GreyScale Effect](Data/GeneratedVisualisations/Effects/Effect_GreyScale.jpg)

   - RGB2BGR

     ![RGB2BGR Effect](Data/GeneratedVisualisations/Effects/Effect_RGB2BGR.jpg)

   - RedChannel

     ![RedChannel Effect](Data/GeneratedVisualisations/Effects/Effect_RedChannel.jpg)

   - BlueChannel

     ![BlueChannel Effect](Data/GeneratedVisualisations/Effects/Effect_BlueChannel.jpg)

   - GreenChannel

     ![GreenChannel Effect](Data/GeneratedVisualisations/Effects/Effect_GreenChannel.jpg)

   - MostDominantColor

     ![MostDominantColor Effect](Data/GeneratedVisualisations/Effects/Effect_MostDominantColor.jpg)

   - LeastDominantColor

     ![LeastDominantColor Effect](Data/GeneratedVisualisations/Effects/Effect_LeastDominantColor.jpg)

   - ScaleValues

     ![ScaleValues Effect](Data/GeneratedVisualisations/Effects/Effect_ScaleValues.jpg)

   - ClipValues

     ![ClipValues Effect](Data/GeneratedVisualisations/Effects/Effect_ClipValues.jpg)

   - BinValues

     ![BinValues Effect](Data/GeneratedVisualisations/Effects/Effect_BinValues.jpg)

   - ResizeBlur

     ![ResizeBlur Effect](Data/GeneratedVisualisations/Effects/Effect_ResizeBlur.jpg)

   - AddFrame

     ![AddFrame Effect](Data/GeneratedVisualisations/Effects/Effect_AddFrame.jpg)

   - GaussianNoise

     ![GaussianNoise Effect](Data/GeneratedVisualisations/Effects/Effect_GaussianNoise.jpg)

   - SpeckleNoise

     ![SpeckleNoise Effect](Data/GeneratedVisualisations/Effects/Effect_SpeckleNoise.jpg)

   - SaltPepperNoise

     ![SaltPepperNoise Effect](Data/GeneratedVisualisations/Effects/Effect_SaltPepperNoise.jpg)

   - SemanticSegmentation

     ![SemanticSegmentation Effect](Data/GeneratedVisualisations/Effects/Effect_SemanticSegmentation.jpg)

   - InstanceSegmentation

     ![InstanceSegmentation Effect](Data/GeneratedVisualisations/Effects/Effect_InstanceSegmentation.jpg)

   - CannyEdges

     ![CannyEdges Effect](Data/GeneratedVisualisations/Effects/Effect_CannyEdges.jpg)

   - ValueCount Plot

     ![ValueCount Effect](Data/GeneratedVisualisations/Effects/Effect_ValueCount.jpg)

   - FrameDelay

     ![FrameDelay Effect](Data/GeneratedVisualisations/Effects/Effect_FrameDelay.gif)

   - And many more! :O
   
     For full list of effects with their parameters see [Effect List](StreamLitGUI/Effects.txt).