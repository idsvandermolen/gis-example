import './style.css';
import { Map, View } from 'ol';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import { fromLonLat, transformExtent } from 'ol/proj';
import GeoJSON from 'ol/format/GeoJSON';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import { bbox as bboxStrategy } from 'ol/loadingstrategy';

const vectorSource = new VectorSource({
  format: new GeoJSON({
    // De meeste Django databases slaan data op in 4326 (graden)
    // OpenLayers toont het standaard in 3857 (meters)
    dataProjection: 'EPSG:4326',
    featureProjection: 'EPSG:3857'
  }),
  strategy: bboxStrategy, // Zorgt dat de loader wordt aangeroepen bij schuiven/zoomen
  loader: function (extent, resolution, projection) {
    // Transformeer de extent van de kaart (EPSG:3857) naar graden (EPSG:4326)
    const extentWGS84 = transformExtent(extent, projection, 'EPSG:4326');
    // Bouw de BBOX URL voor DRF (minx,miny,maxx,maxy)
    const baseUrl = `http://localhost:8000/api/?in_bbox=${extentWGS84.join(',')}`;

    // Recursieve functie om alle pagina's op te halen
    const loadPages = (url) => {
      fetch(url)
        .then(response => response.json())
        .then(data => {
          // Voeg de features van deze pagina toe
          const features = vectorSource.getFormat().readFeatures(data, {
            featureProjection: projection,
          });
          vectorSource.addFeatures(features);

          // Is er een volgende pagina? Haal die dan ook op
          if (data.next) {
            // DRF geeft vaak een volledige URL in 'next'
            loadPages(data.next);
          }
        });
    };

    loadPages(baseUrl);
  },
});

const map = new Map({
  target: 'map',
  layers: [
    new TileLayer({
      source: new OSM()
    }),
    new VectorLayer({
      source: vectorSource
    }),
  ],
  view: new View({
    center: fromLonLat([5.29, 52.13]), // Midden van Nederland
    zoom: 7
  })
});
