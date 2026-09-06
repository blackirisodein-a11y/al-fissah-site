#!/bin/bash
cd "$(dirname "$0")"
echo ""
echo "  AL-FISSAH — serveur local"
echo "  -------------------------"
echo "  Le site s'ouvre dans votre navigateur."
echo "  Laissez cette fenêtre ouverte. Pour arrêter : Ctrl+C."
echo ""
(sleep 1 && (open http://localhost:8000 2>/dev/null || xdg-open http://localhost:8000 2>/dev/null)) &
python3 -m http.server 8000
