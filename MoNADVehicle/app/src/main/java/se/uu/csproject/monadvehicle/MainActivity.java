package se.uu.csproject.monadvehicle;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.graphics.drawable.Drawable;
import android.location.Location;
import android.media.Image;
import android.os.Environment;
import android.os.Bundle;
import android.support.v4.content.ContextCompat;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.GoogleApiClient.ConnectionCallbacks;
import com.google.android.gms.common.api.GoogleApiClient.OnConnectionFailedListener;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;

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
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.List;


public class MainActivity extends Activity implements ConnectionCallbacks, OnConnectionFailedListener{

    LinearLayout sideList;
    Route route;
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

    /**
     * The desired interval for location updates. Inexact. Updates may be more or less frequent.
     */
    public static final long UPDATE_INTERVAL_IN_MILLISECONDS = 1000;

    /**
     * The fastest rate for active location updates. Exact. Updates will never be more frequent
     * than this value.
     */
    public static final long FASTEST_UPDATE_INTERVAL_IN_MILLISECONDS =
            UPDATE_INTERVAL_IN_MILLISECONDS / 2;

    /**
     * Provides the entry point to Google Play services.
     */
    protected GoogleApiClient mGoogleApiClient;

    /**
     * Stores parameters for requests to the FusedLocationProviderApi.
     */
    protected LocationRequest mLocationRequest;

    /**
     * Represents a geographical location.
     */
    protected Location mCurrentLocation;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        sideList = (LinearLayout) findViewById(R.id.side_list);
        route = new Route(generateBusStops());

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

        //the bitmap that shows the current location
        Drawable drawable = ContextCompat.getDrawable(getBaseContext(), R.drawable.marker_red);
        Bitmap bitmap = AndroidGraphicFactory.convertToBitmap(drawable);

        myLocationOverlay = new MyLocationOverlay(this, this.mapView.getModel().mapViewPosition, bitmap);
        myLocationOverlay.setSnapToLocationEnabled(false);

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

        //// TODO: receive route from server and draw it. The following route is just for demo.
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

        buildGoogleApiClient();

        ImageButton showBusStopList =(ImageButton)findViewById(R.id.busStopButton);
        showBusStopList.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sideList.setVisibility(View.VISIBLE);
                LayoutInflater inflater = (LayoutInflater) getApplicationContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
                ViewGroup insertPoint = (ViewGroup) findViewById(R.id.side_list);

                for (int j = 0; j < route.getBusStopList().size(); j++) {
                    View busStopView = inflater.inflate(R.layout.list_item_busstop, null);
                    TextView busStopTime = (TextView) busStopView.findViewById(R.id.text_busstoptime);
                    TextView busStopName = (TextView) busStopView.findViewById(R.id.text_busstopname);
                    busStopTime.setText(formatTime(route.getBusStopList().get(j).getArrivalTime()));
                    busStopName.setText(route.getBusStopList().get(j).getName());
                    insertPoint.addView(busStopView);
                }
            }
        });
    }

    @Override
    protected void onPause(){
        super.onPause();

        if(mGoogleApiClient.isConnected()) {
            stopLocationUpdates();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();

        if(mGoogleApiClient.isConnected()) {
            myLocationOverlay.enableMyLocation(true);
            startLocationUpdates();
        }
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
        mGoogleApiClient.connect();
    }

    @Override
    protected void onStop(){
        mGoogleApiClient.disconnect();

        super.onStop();
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

    @Override
    public void onConnected(Bundle bundle) {
        myLocationOverlay.enableMyLocation(true);
        startLocationUpdates();
    }

    @Override
    public void onConnectionSuspended(int i) {
        // The connection to Google Play services was lost for some reason. We call connect() to
        // attempt to re-establish the connection.
        Log.i("OBS", "Connection suspended");
        mGoogleApiClient.connect();
    }

    @Override
    public void onConnectionFailed(ConnectionResult connectionResult) {
        Log.i("ERROR", "Connection failed: ConnectionResult.getErrorCode() = " + connectionResult.getErrorCode());
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Warning");
        builder.setMessage("We cannot get your current location because your Google Play Service is out-of-date, please update it.");
        // Add the buttons
        builder.setNegativeButton("OK", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int id) {
                // User cancelled the dialog
                //do nothing
            }
        });
        AlertDialog dialog = builder.create();
        dialog.show();
    }

    /**
     * Builds a GoogleApiClient. Uses the {@code #addApi} method to request the
     * LocationServices API.
     */
    protected synchronized void buildGoogleApiClient() {
        //Log.i(TAG, "Building GoogleApiClient");
        mGoogleApiClient = new GoogleApiClient.Builder(this)
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this)
                .addApi(LocationServices.API)
                .build();
        createLocationRequest();
    }

    protected void createLocationRequest() {
        mLocationRequest = new LocationRequest();

        // Sets the desired interval for active location updates. This interval is
        // inexact. You may not receive updates at all if no location sources are available, or
        // you may receive them slower than requested. You may also receive updates faster than
        // requested if other applications are requesting location at a faster interval.
        mLocationRequest.setInterval(UPDATE_INTERVAL_IN_MILLISECONDS);

        // Sets the fastest rate for active location updates. This interval is exact, and your
        // application will never receive updates faster than this value.
        mLocationRequest.setFastestInterval(FASTEST_UPDATE_INTERVAL_IN_MILLISECONDS);

        mLocationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
    }

    /**
     * Requests location updates from the FusedLocationApi.
     */
    protected void startLocationUpdates() {
        // The final argument to {@code requestLocationUpdates()} is a LocationListener
        // (http://developer.android.com/reference/com/google/android/gms/location/LocationListener.html).
        LocationServices.FusedLocationApi.requestLocationUpdates(mGoogleApiClient, mLocationRequest, myLocationOverlay);
    }

    /**
     * Removes location updates from the FusedLocationApi.
     */
    protected void stopLocationUpdates() {
        // It is a good practice to remove location requests when the activity is in a paused or
        // stopped state. Doing so helps battery performance and is especially
        // recommended in applications that request frequent location updates.

        // The final argument to {@code requestLocationUpdates()} is a LocationListener
        // (http://developer.android.com/reference/com/google/android/gms/location/LocationListener.html).
        LocationServices.FusedLocationApi.removeLocationUpdates(mGoogleApiClient, myLocationOverlay);
    }

    private String formatTime(Date arrival) {
        final String TIME_FORMAT = "HH:mm";
        SimpleDateFormat timeFormat = new SimpleDateFormat(TIME_FORMAT);
        return timeFormat.format(arrival);
    }

    public ArrayList<BusStop> generateBusStops(){
        ArrayList<BusStop> busStops = new ArrayList<>();
        Calendar calendar = new GregorianCalendar(2015, 11, 23, 15, 0, 0);
        Date arrival1 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 11, 23, 15, 5, 0);
        Date arrival2 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 11, 23, 15, 10, 0);
        Date arrival3 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 11, 23, 15, 20, 0);
        Date arrival4 = calendar.getTime();

        BusStop stop1 = new BusStop(1, "Centralstation", 0, 0, arrival1, 2, 0);
        busStops.add(stop1);
        BusStop stop2 = new BusStop(1, "Centralstation", 0, 0, arrival2, 1, 1);
        busStops.add(stop2);
        BusStop stop3 = new BusStop(1, "Centralstation", 0, 0, arrival3, 3, 4);
        busStops.add(stop3);
        BusStop stop4 = new BusStop(1, "Centralstation", 0, 0, arrival4, 0, 1);
        busStops.add(stop4);

        return busStops;
    }
}