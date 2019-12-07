# Node-RED Flow

Node-RED flow integrating the low-level LED strip control with various data sources and APIs. To be deployed on the Raspberry Pi that's powering the LED strip.

## Prerequisites

1. Install [Node-RED](https://nodered.org/docs/hardware/raspberrypi)
2. Modify `~/.node-red/settings.js`:
   1. `flowFile: <absolute path to this directory's iotree-flows.json>,`
   2. `flowFilePretty: true,`
   3. `credentialSecret: <some random value>,`
3. Install nodes:
   1. `node-red-dashboard`