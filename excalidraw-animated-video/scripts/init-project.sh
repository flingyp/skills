#!/bin/bash

set -e

PROJECT_NAME=${1:-"excalidraw-video"}
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATE_DIR="$SKILL_DIR/assets/template"

if [ -d "$PROJECT_NAME" ]; then
    echo "Error: Directory '$PROJECT_NAME' already exists"
    exit 1
fi

echo "Creating Excalidraw Animated Video project: $PROJECT_NAME"

mkdir -p "$PROJECT_NAME"/{src/{components,types,compositions},excalidraw,public/fonts,out}

cp -r "$TEMPLATE_DIR/src/"* "$PROJECT_NAME/src/"
cp "$TEMPLATE_DIR/package.json" "$PROJECT_NAME/"
cp "$TEMPLATE_DIR/tsconfig.json" "$PROJECT_NAME/"

cat > "$PROJECT_NAME/storyboard.json" << 'EOF'
{
  "title": "手绘动画视频",
  "duration": 30,
  "scenes": [
    {
      "id": "scene-1",
      "title": "开场",
      "voiceover": "欢迎观看本期视频",
      "duration": 5,
      "diagramType": "freeform"
    },
    {
      "id": "scene-2",
      "title": "核心内容",
      "voiceover": "这是核心内容讲解",
      "duration": 15,
      "diagramType": "flowchart"
    },
    {
      "id": "scene-3",
      "title": "结尾",
      "voiceover": "感谢观看",
      "duration": 5,
      "diagramType": "freeform"
    }
  ]
}
EOF

cat > "$PROJECT_NAME/remotion.config.ts" << 'EOF'
import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
EOF

cat > "$PROJECT_NAME/README.md" << 'EOF'
# Excalidraw Animated Video

手绘风格动画讲解视频项目。

## 开发

```bash
npm install
npm start
```

## 渲染

```bash
npm run build        # MP4
npm run build:webm   # WebM
```

## 结构

- `excalidraw/` - Excalidraw 场景文件
- `src/` - Remotion 源码
- `out/` - 输出视频
EOF

echo ""
echo "✅ Project created: $PROJECT_NAME"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  npm install"
echo "  npm start"
