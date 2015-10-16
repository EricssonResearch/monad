package se.uu.csproject.monadvehicle;

import android.app.Activity;
import android.content.Context;
import android.graphics.drawable.Drawable;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Environment;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;

import org.mapsforge.core.graphics.Bitmap;
import org.mapsforge.core.graphics.Color;
import org.mapsforge.core.graphics.Paint;
import org.mapsforge.core.graphics.Style;
import org.mapsforge.core.model.LatLong;
import org.mapsforge.map.android.graphics.AndroidGraphicFactory;
import org.mapsforge.map.android.util.AndroidUtil;
import org.mapsforge.map.android.view.MapView;
import org.mapsforge.map.layer.cache.TileCache;
import org.mapsforge.map.layer.overlay.Polyline;
import org.mapsforge.map.layer.renderer.TileRendererLayer;
import org.mapsforge.map.reader.MapDataStore;
import org.mapsforge.map.reader.MapFile;
import org.mapsforge.map.rendertheme.InternalRenderTheme;

import java.io.File;
import java.util.List;


public class MainActivity extends Activity {

    // name of the map file in the external storage, it should be stored in the root directory of the sdcard
    private static final String MAPFILE = "uppsala.map";
    // MapView provided by mapsforge instead of native MapView in Android
    private MapView mapView;
    // cache to store tiles
    private TileCache tileCache;
    // this layer displays tiles from local map file
    private TileRendererLayer tileRendererLayer;
    // this layer shows the current location of the bus
    private MyLocationOverlay myLocationOverlay;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mapView = (MapView) findViewById(R.id.mapView);

        //setup mapView
        mapView.setClickable(true);
        mapView.getMapScaleBar().setVisible(true);
        mapView.setBuiltInZoomControls(true);
        mapView.getMapZoomControls().setZoomLevelMin((byte) 10);
        mapView.getMapZoomControls().setZoomLevelMax((byte) 20);
        // the cente should be the current location, but now it's just in flogsta
        mapView.getModel().mapViewPosition.setCenter(new LatLong(59.851294, 17.593113));
        mapView.getModel().mapViewPosition.setZoomLevel((byte) 12);

        // create a tile cache of suitable size
        this.tileCache = AndroidUtil.createTileCache(this, "mapcache",
                mapView.getModel().displayModel.getTileSize(), 1f,
                this.mapView.getModel().frameBufferModel.getOverdrawFactor());

        LocationManager locationManager=(LocationManager)getSystemService(Context.LOCATION_SERVICE);

        //the bitmap that shows the current location
        Drawable drawable = getResources().getDrawable(R.drawable.marker_red);
        Bitmap bitmap = AndroidGraphicFactory.convertToBitmap(drawable);

        myLocationOverlay = new MyLocationOverlay(this, this.mapView.getModel().mapViewPosition, bitmap);
        myLocationOverlay.setSnapToLocationEnabled(false);

        // since API 23, runtime check of permission is required
        try {
            //locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0, (LocationListener) myLocationOverlay);
            locationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 20, 0, (LocationListener) myLocationOverlay);
        } catch (SecurityException e){
            Log.e("Exception", e.getMessage());
        }

        // tile renderer layer using internal render theme
        MapDataStore mapDataStore = new MapFile(getMapFile());
        this.tileRendererLayer = new TileRendererLayer(tileCache, mapDataStore,
                this.mapView.getModel().mapViewPosition, false, true, AndroidGraphicFactory.INSTANCE);
        tileRendererLayer.setXmlRenderTheme(InternalRenderTheme.OSMARENDER);

        // only once a layer is associated with a mapView the rendering starts
        this.mapView.getLayerManager().getLayers().add(tileRendererLayer);

        // instantiating the paint object
        Paint paint = AndroidGraphicFactory.INSTANCE.createPaint();
        paint.setColor(Color.RED);
        paint.setStrokeWidth(10);
        paint.setStyle(Style.STROKE);

        // instantiating the polyline object
        Polyline polyline = new Polyline(paint, AndroidGraphicFactory.INSTANCE);

        // the route from polacksbacken to flogsta
        // to draw the route, all the turning points along the route must be specified,
        // mapsforge does not have the functionality to draw the route between two points with auto detection of turning points
        List<LatLong> coordinateList = polyline.getLatLongs();
        coordinateList.add(new LatLong(59.851294, 17.593113));
        coordinateList.add(new LatLong(59.850208, 17.600629));
        coordinateList.add(new LatLong(59.851952, 17.603680));
        coordinateList.add(new LatLong(59.850008, 17.610965));
        coordinateList.add(new LatLong(59.852265, 17.613409));
        coordinateList.add(new LatLong(59.853481, 17.616570));
        coordinateList.add(new LatLong(59.850975, 17.618847));
        coordinateList.add(new LatLong(59.849815, 17.620939));
        coordinateList.add(new LatLong(59.846652, 17.624497));
        coordinateList.add(new LatLong(59.846425, 17.624276));
        coordinateList.add(new LatLong(59.844812, 17.625015));
        coordinateList.add(new LatLong(59.840875, 17.630646));
        coordinateList.add(new LatLong(59.841609, 17.639105));
        coordinateList.add(new LatLong(59.839344, 17.640161));
        coordinateList.add(new LatLong(59.840673, 17.647350));
        coordinateList.add(new LatLong(59.840063, 17.647760));

        // adding the layer with the route to the mapview
        mapView.getLayerManager().getLayers().add(polyline);

        // adding the layer with current location to the mapview
        mapView.getLayerManager().getLayers().add(this.myLocationOverlay);
    }

    @Override
    protected void onResume() {
        super.onResume();

        myLocationOverlay.enableMyLocation(false);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    protected void onStart() {
        super.onStart();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        this.mapView.destroyAll();
    }

    /**
     * Get the local map file
     *
     * @return the local map file as a File type
     */
    private File getMapFile() {
        File file = new File(Environment.getExternalStorageDirectory(), MAPFILE);
        return file;
    }
}
