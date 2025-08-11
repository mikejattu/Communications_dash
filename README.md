# Oil Sands Level Monitoring Dashboard

![Dashboard Preview](https://example.com/path/to/screenshot.png) *<!-- Add actual screenshot URL -->*

An industrial-grade web application combining **computer vision** and **OPC UA communication** for real-time oil sands level monitoring and control.

## Key Features

### 🎯 Core Capabilities
- **Real-time level measurement** using computer vision algorithms
- **Confidence scoring** (0-100%) for measurement reliability
- **Automated fallback system** switches to predefined logic when confidence < threshold
- **Multi-camera support** with adjustable pitch/yaw controls

### 🖥️ OPC UA Integration
- **Secure server connections** with authentication
- **Node management** for:
  - `LevelNode` - Current material level value
  - `ConfidenceNode` - Measurement certainty score  
  - `SetpointNode` - Target level reference
  - `SwitchNode` - AI/Fallback mode toggle
- **Live data subscription** with 1-second refresh
- **Command terminal** for direct node interaction

### 📊 Visualization
- **Real-time graphing** of level/confidence trends
- **Event logging** with timestamped alerts
- **Camera feed display** with measurement overlays
- **Responsive dashboard** adapts to screen size

### ⚙️ Configuration
- **Server management**:
  - Endpoint URL configuration
  - Credential storage
  - Connection status monitoring
- **Node customization**:
  - Subscription management
  - Threshold adjustments
- **Camera calibration**:
  - Tilt/pan controls
  - FOV adjustment

## Technology Stack
| Component       | Technology |
|-----------------|------------|
| Frontend        | Dash (Python) |
| Computer Vision | OpenCV/PyTorch |
| OPC UA Client   | asyncua |
| Visualization   | Plotly |
| UI Components   | Dash Bootstrap Components |

## Getting Started

### Prerequisites
- Python 3.8+
- OPC UA server endpoint
- RTSP/IP camera feed
