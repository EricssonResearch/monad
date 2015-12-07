package se.uu.csproject.monadvehicle;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.graphics.drawable.Drawable;
import android.location.Location;
import android.os.AsyncTask;
import android.os.Environment;
import android.os.Bundle;
import android.support.v4.content.ContextCompat;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.RadioGroup;
import android.widget.ScrollView;
import android.widget.TextView;

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
import org.mapsforge.core.model.BoundingBox;
import org.mapsforge.core.model.LatLong;
import org.mapsforge.map.android.graphics.AndroidGraphicFactory;
import org.mapsforge.map.android.util.AndroidUtil;
import org.mapsforge.map.android.view.MapView;
import org.mapsforge.map.layer.cache.TileCache;
import org.mapsforge.map.layer.overlay.Marker;
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
import java.util.concurrent.TimeUnit;


public class MainActivity extends Activity implements ConnectionCallbacks, OnConnectionFailedListener,
        AsyncGetTrafficInformationInteraction {

    // Interface variables
    LinearLayout sideList, notificationsList, busStopsList, emergencyList;
    ScrollView notificationsScroll, busStopScroll;
    RadioGroup radioGroup;
    CheckBox otherCheckBox;
    EditText emergencyDescription;

    NotificationList notifications;
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

    //The desired interval for location updates. Inexact. Updates may be more or less frequent.
    public static final long UPDATE_INTERVAL_IN_MILLISECONDS = 1000;

    //The fastest rate for active location updates. Exact.
    // Updates will never be more frequent than this value.
    public static final long FASTEST_UPDATE_INTERVAL_IN_MILLISECONDS =
            UPDATE_INTERVAL_IN_MILLISECONDS / 2;

    //Provides the entry point to Google Play services.
    protected GoogleApiClient mGoogleApiClient;

    //Stores parameters for requests to the FusedLocationProviderApi.
    protected LocationRequest mLocationRequest;

    // Represents a geographical location.
    //protected Location mCurrentLocation;

    //for distance and time calculations
    Location location;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        sideList = (LinearLayout) findViewById(R.id.side_list);
        notificationsList = (LinearLayout) findViewById(R.id.side_list_notifications);
        busStopsList = (LinearLayout) findViewById(R.id.side_list_busstops);
        emergencyList = (LinearLayout) findViewById(R.id.side_list_emergency);
        notificationsScroll = (ScrollView) findViewById(R.id.side_list_notifications_scroll);
        busStopScroll = (ScrollView) findViewById(R.id.side_list_busstops_scroll);
        notifications = new NotificationList(generateNotifications());
        emergencyDescription = (EditText) findViewById(R.id.text_description);

        //Fill the notifications list
        LayoutInflater inflater = (LayoutInflater) getApplicationContext().getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        for (int j = 0; j < notifications.getNotificationsList().size(); j++) {
            View notificationView = inflater.inflate(R.layout.list_item_notification, null);
            TextView incomingTime = (TextView) notificationView.findViewById(R.id.text_incomingtime);
            TextView message = (TextView) notificationView.findViewById(R.id.text_message);
            incomingTime.setText(formatTime(notifications.getNotificationsList().get(j).getIncomingTime()));
            message.setText(notifications.getNotificationsList().get(j).getMessage());
            notificationsList.addView(notificationView);
        }

        //Fill the bus stop list
        for (int j = 0; j < Storage.getBusTrip().getBusStops().size(); j++) {
            View busStopView = inflater.inflate(R.layout.list_item_busstop, null);
            TextView busStopTime = (TextView) busStopView.findViewById(R.id.text_busstoptime);
            TextView busStopName = (TextView) busStopView.findViewById(R.id.text_busstopname);
            busStopTime.setText(formatTime(Storage.getBusTrip().getBusStops().get(j).getArrivalTime()));
            busStopName.setText(Storage.getBusTrip().getBusStops().get(j).getName());
            busStopsList.addView(busStopView);
        }

        //Set up mapView
        mapView = (MapView) findViewById(R.id.mapView);
        mapView.setClickable(true);
        mapView.getMapScaleBar().setVisible(true);
        mapView.setBuiltInZoomControls(true);
        mapView.getMapZoomControls().setZoomLevelMin((byte) 12);
        mapView.getMapZoomControls().setZoomLevelMax((byte) 20);
        // Setting the center of the map before user location is detected
        // Coordinates lat=59.8586, lon=17.6461 are Uppsala Central Station
        mapView.getModel().mapViewPosition.setCenter(new LatLong(59.8586, 17.6461));
        mapView.getModel().mapViewPosition.setZoomLevel((byte) 12);
        // Set the boundaries of the map. Values taken from Uppsala.map
        mapView.getModel().mapViewPosition.setMapLimit(
                new BoundingBox(59.7541, 17.392, 59.9086, 17.9039)
        );
        // create a tile cache of suitable size
        this.tileCache = AndroidUtil.createTileCache(this, "mapcache",
                mapView.getModel().displayModel.getTileSize(), 1f,
                this.mapView.getModel().frameBufferModel.getOverdrawFactor());

        //the bitmap that shows the current location
        Drawable drawable = ContextCompat.getDrawable(getBaseContext(), R.drawable.marker_blue);
        Bitmap bitmap = AndroidGraphicFactory.convertToBitmap(drawable);

        //the bitmap used for bus stops
        drawable = ContextCompat.getDrawable(getBaseContext(), R.mipmap.ic_directions_bus_black_18dp);
        Bitmap busBitmap = AndroidGraphicFactory.convertToBitmap(drawable);

        myLocationOverlay = new MyLocationOverlay(this, this.mapView.getModel().mapViewPosition, bitmap);
        myLocationOverlay.setSnapToLocationEnabled(false);

        //for simulation
        myLocationOverlay.trajectory = Storage.getBusTrip().getTrajectory();

        // tile renderer layer using internal render theme
        MapDataStore mapDataStore = new MapFile(getMapFile());
        this.tileRendererLayer = new TileRendererLayer(tileCache, mapDataStore,
                this.mapView.getModel().mapViewPosition, false, true, AndroidGraphicFactory.INSTANCE);
        tileRendererLayer.setXmlRenderTheme(InternalRenderTheme.OSMARENDER);

        // only once a layer is associated with a mapView the rendering starts
        this.mapView.getLayerManager().getLayers().add(tileRendererLayer);

        // Drawing the route using the trajectory stored in busTrip
        Paint paint = AndroidGraphicFactory.INSTANCE.createPaint();
        paint.setColor(Color.RED);
        paint.setStrokeWidth(10);
        paint.setStyle(Style.STROKE);
        Polyline polyline = new Polyline(paint, AndroidGraphicFactory.INSTANCE);
        List<LatLong> coordinateList = polyline.getLatLongs();
        for (int i = 0; i < Storage.getBusTrip().getTrajectory().size(); i++) {
            coordinateList.add(Storage.getBusTrip().getTrajectory().get(i));
        }

        // adding the layer with the route to the mapview
        mapView.getLayerManager().getLayers().add(polyline);
        // adding the layer with current location to the mapview
        mapView.getLayerManager().getLayers().add(this.myLocationOverlay);
        // adding a marker for each bus stop to the mapview
        for(int i = 0; i < Storage.getBusTrip().getBusStops().size(); i++) {
            mapView.getLayerManager().getLayers().add(new Marker(Storage.getBusTrip().getBusStops().get(i).getLatLong(), busBitmap, 0, 0));
        }

        buildGoogleApiClient();

        getTrafficInformation();

        /*
         * Click listeners to manage the side list buttons
         */
        ImageButton showBusStopList =(ImageButton)findViewById(R.id.busStopButton);
        showBusStopList.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (busStopScroll.getVisibility() == View.VISIBLE) {
                    busStopScroll.setVisibility(View.GONE);
                    sideList.setVisibility(View.GONE);
                } else if (notificationsScroll.getVisibility() == View.VISIBLE
                        || emergencyList.getVisibility() == View.VISIBLE) {
                    notificationsScroll.setVisibility(View.GONE);
                    emergencyList.setVisibility(View.GONE);
                    busStopScroll.setVisibility(View.VISIBLE);
                } else {
                    sideList.setVisibility(View.VISIBLE);
                    busStopScroll.setVisibility(View.VISIBLE);
                }
            }
        });



        ImageButton showNotificationsList =(ImageButton)findViewById(R.id.notificationButton);
        showNotificationsList.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(notificationsScroll.getVisibility() == View.VISIBLE){
                    notificationsScroll.setVisibility(View.GONE);
                    sideList.setVisibility(View.GONE);
                }
                else if (busStopScroll.getVisibility() == View.VISIBLE
                        || emergencyList.getVisibility() == View.VISIBLE){
                    busStopScroll.setVisibility(View.GONE);
                    emergencyList.setVisibility(View.GONE);
                    notificationsScroll.setVisibility(View.VISIBLE);
                }
                else {
                    sideList.setVisibility(View.VISIBLE);
                    notificationsScroll.setVisibility(View.VISIBLE);
                }
            }
        });

        ImageButton showEmergencyList =(ImageButton)findViewById(R.id.emergencyButton);
        showEmergencyList.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (emergencyList.getVisibility() == View.VISIBLE) {
                    emergencyList.setVisibility(View.GONE);
                    sideList.setVisibility(View.GONE);
                } else if (notificationsScroll.getVisibility() == View.VISIBLE
                        || busStopScroll.getVisibility() == View.VISIBLE) {
                    notificationsScroll.setVisibility(View.GONE);
                    busStopScroll.setVisibility(View.GONE);
                    emergencyList.setVisibility(View.VISIBLE);
                } else {
                    sideList.setVisibility(View.VISIBLE);
                    emergencyList.setVisibility(View.VISIBLE);
                }
            }
        });

        /*
         * Checkbox and Radio listeners to handle options in the emergency screen
         */
        otherCheckBox = (CheckBox) findViewById(R.id.other_possiblity);
        otherCheckBox.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
                public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    emergencyDescription.setEnabled(true);
                }
                else {
                    emergencyDescription.setEnabled(false);
                }
            }
        });

        radioGroup = (RadioGroup) findViewById(R.id.radio_emergency);
        radioGroup.clearCheck();
        radioGroup.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                if (checkedId == R.id.radio_otherissue) {
                    otherCheckBox.setChecked(true);
                    emergencyDescription.setEnabled(true);
                }
                else {
                    otherCheckBox.setChecked(true);
                    emergencyDescription.setEnabled(false);
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

        if (mGoogleApiClient.isConnected()) {
            myLocationOverlay.enableMyLocation(true);
            //commented since simulation is used now instead of real location
            //startLocationUpdates();
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
        return new File(Environment.getExternalStorageDirectory(), MAPFILE);
    }

    @Override
    public void onConnected(Bundle bundle) {
        myLocationOverlay.enableMyLocation(true);

        //manually simulate the movement of the bus
        myLocationOverlay.moveSimulate();

        //commented since simulation is used now instead of real location
        //startLocationUpdates();

        //updates the distance and time
        calculateDistance();
        calculateTimeDifference();
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

    public ArrayList<Notification> generateNotifications(){
        ArrayList<Notification> notifications = new ArrayList<>();
        Calendar calendar = new GregorianCalendar(2015, 11, 23, 15, 0, 0);
        Date arrival1 = calendar.getTime();
        calendar = new GregorianCalendar(2015, 11, 23, 15, 5, 0);
        Date arrival2 = calendar.getTime();
        Notification message;

        for(int i=0; i<7; i++) {
            message = new Notification(i, "Updated route", arrival1);
            notifications.add(message);
            message = new Notification(i, "Route Cancelled", arrival2);
            notifications.add(message);
        }
        return notifications;
    }

    //gets the current location of the bus and the next bus stop
    //calculates the distance between them and sets it to the text box.
    public void calculateDistance() {
        Location location=new Location("");
        Location destLocation = new Location("");
        myLocationOverlay.onLocationChanged(location);
        double currentLat = location.getLatitude();
        double currentLong = location.getLongitude();
        //location.setLatitude(currentLat);
        //location.setLongitude(currentLong);
        destLocation.setLatitude(Storage.getBusTrip().getBusStops().get(1).getLatitude());
        destLocation.setLongitude(Storage.getBusTrip().getBusStops().get(1).getLongitude());
        TextView textViewDistance = (TextView)findViewById(R.id.text_distanceRemaining);
        String distance = Double.toString(location.distanceTo(destLocation));
        textViewDistance.setText(distance);
    }

    //gets the current time of the bus and the next bus stop
    //arrival time and calculates the remaining time between
    //current location time and next bus stop and sets it to the text box.
    public void calculateTimeDifference() {
        Location location=new Location("");
        myLocationOverlay.onLocationChanged(location);
        Calendar cal = Calendar.getInstance();
        long currentTime = cal.get(Calendar.MILLISECOND);
        TextView textViewMinutes = (TextView)findViewById(R.id.text_timeRemaining);
        String minutes = Long.toString(TimeUnit.MILLISECONDS.toMinutes(Storage.getBusTrip().getBusStops().get(1).getArrivalTime().getTime() - currentTime));
        textViewMinutes.setText(minutes);
    }

    public void getTrafficInformation() {

        if (Storage.isEmptyTrafficIncidents()) {
            new GetTrafficInformationTask(this).executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
        }
    }

    @Override
    public void processReceivedGetTrafficInformationResponse(String response) {

        if (response.equals("1")) {
            Log.d("MainActivity", "Successfully received TrafficInformation data");
            Storage.printTrafficIncidents();
        } else {
            Log.d("MainActivity", "Error while receiving TrafficInformation data");
        }
    }
}