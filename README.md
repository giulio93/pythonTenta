# Cloud_To_Matter_Border_Router
## Requirements
- arduino/chip-tool docker image
- arduino/otbr docker image

## Instructions
- In the portenta
  - adb push the matterTool.sh to the portenta
  - copy the matterTool.sh script under /usr/sbin/mattertool
- Build in your PC the image
  - docker build -t giulionepasticcione/portenta-router:v2.0 . && docker push giulionepasticcione/portenta-router:v2.0
- Pull it from the portenta
  - adb push the docker compose to the portenta
  - docker pull giulionepasticcione/portenta-router:v2.0 && docker compose up