<script>
  import { onMount } from 'svelte';
  import L from 'leaflet';


  let currentStepIndex = 0;
  let map;
  let polylineLayer;

  onMount(() => {
    map = L.map('map').setView([35.681219, 139.767193], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    drawStep();
  });

  function drawStep() {
    if (polylineLayer) {
      map.removeLayer(polylineLayer);
    }

    const step = segments[0].steps[currentStepIndex];
    const [startIndex, endIndex] = step.way_points;

    const stepCoords = coordinates.slice(startIndex, endIndex + 1).map(coord => [coord[1], coord[0]]); // 緯度経度順に変換
    polylineLayer = L.polyline(stepCoords, { weight: 5 }).addTo(map);
    map.fitBounds(polylineLayer.getBounds());
  }

  function nextStep() {
    if (currentStepIndex < segments[0].steps.length - 1) {
      currentStepIndex++;
      drawStep();
    } else {
      alert('最後のステップです！');
    }
  }
</script>

<div id="map" style="height: 400px;"></div>
<button on:click={nextStep}>次へ</button>
