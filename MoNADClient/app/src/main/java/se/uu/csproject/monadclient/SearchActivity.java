package se.uu.csproject.monadclient;

import android.Manifest;
import android.app.DatePickerDialog;
import android.app.Dialog;
import android.app.DialogFragment;
import android.app.TimePickerDialog;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.os.Build;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.text.format.DateFormat;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;
import android.view.inputmethod.InputMethodManager;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.TimePicker;
import android.widget.Toast;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GoogleApiAvailability;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

import se.uu.csproject.monadclient.recyclerviews.FullTrip;
import se.uu.csproject.monadclient.recyclerviews.SearchRecyclerViewAdapter;
import se.uu.csproject.monadclient.recyclerviews.Storage;

public class SearchActivity extends MenuedActivity implements
        GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener, LocationListener, AsyncResponse{
    private TextView textViewTripDate, textViewTripTime;
    DialogFragment dateFragment;
    DialogFragment timeFragment;
    private RadioGroup tripTimeRadioGroup, priorityRadioGroup;
    private EditText positionEditText, destinationEditText;
    private GoogleApiClient mGoogleApiClient;
    private LocationRequest mLocationRequest;
    private double currentLatitude, currentLongitude;
    private Context context;
    public Calendar calendar;
    private ArrayList<FullTrip> searchResults;
    private SearchRecyclerViewAdapter adapter;
    private LinearLayoutManager linearLayoutManager;
    private RecyclerView recyclerView;
    //private DatePicker datePicker;

    private static final int PLAY_SERVICES_RESOLUTION_REQUEST = 9000;
    private final int MY_PERMISSIONS_REQUEST = 123;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search);
        Toolbar toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);

        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        context = getApplicationContext();
        textViewTripDate = (TextView) findViewById(R.id.textview_search_tripdate);
        calendar = Calendar.getInstance();
        updateDate();
        textViewTripTime= (TextView) findViewById(R.id.textview_search_triptime);
        updateTime();

        textViewTripDate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showDatePickerDialog(v);
            }
        });
        textViewTripTime.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showTimePickerDialog(v);
            }
        });

        tripTimeRadioGroup = (RadioGroup) findViewById(R.id.radiogroup_search_triptime);
        priorityRadioGroup = (RadioGroup) findViewById(R.id.radiogroup_search_priority);
        positionEditText = (EditText) findViewById(R.id.edittext_search_position);
        destinationEditText = (EditText) findViewById(R.id.edittext_search_destination);

        recyclerView = (RecyclerView) findViewById(R.id.recycler_view_search);
        linearLayoutManager = new LinearLayoutManager(getApplicationContext());
        recyclerView.setLayoutManager(linearLayoutManager);

        currentLatitude = 0;
        currentLongitude = 0;

        buildGoogleApiClient();
        initializeLocationRequest();

        // Hide the keyboard when launching this activity
        this.getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_HIDDEN);
    }

    private void checkForPermission(){
        if (ContextCompat.checkSelfPermission(SearchActivity.this, Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED){
            ActivityCompat.requestPermissions(SearchActivity.this,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, MY_PERMISSIONS_REQUEST);
        } else {
            mGoogleApiClient.connect();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        switch (requestCode) {
            case MY_PERMISSIONS_REQUEST: {
                // If request is cancelled, the result arrays are empty.
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    mGoogleApiClient.connect();
                } else {
                    // Permission denied, boo! Disable the functionality that depends on this permission.
                    CharSequence text = "If you don't give location permission then we can't use " +
                            "your current location to search for suitable bus trips.";
                    int duration = Toast.LENGTH_LONG;
                    Toast toast = Toast.makeText(context, text, duration);
                    toast.show();
                }
                return;
            }
        }
    }

    private void handleNewLocation(Location location) {
        currentLatitude = location.getLatitude();
        currentLongitude = location.getLongitude();
    }

    protected synchronized void buildGoogleApiClient() {
        mGoogleApiClient = new GoogleApiClient.Builder(this)
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this)
                .addApi(LocationServices.API)
                .build();
    }

    protected void initializeLocationRequest() {
        mLocationRequest = LocationRequest.create()
                .setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY)
                .setInterval(60 * 1000)        // 1 minute, in milliseconds
                .setFastestInterval(10 * 1000); // 10 seconds, in milliseconds
    }

    public void showDatePickerDialog(View v) {
        dateFragment = new DatePickerFragment();
        dateFragment.show(getFragmentManager(), "datePicker");
    }

    public void showTimePickerDialog(View v) {
        timeFragment = new TimePickerFragment();
        timeFragment.show(getFragmentManager(), "timePicker");
    }

    public void updateDate() {
        final String DATE_FORMAT = "EEE dd MMM";
        SimpleDateFormat dateFormat = new SimpleDateFormat(DATE_FORMAT);
        String selectedDate = dateFormat.format(calendar.getTime());
        textViewTripDate.setText(selectedDate);
    }

    public void updateTime() {
        final String TIME_FORMAT = "HH:mm";
        SimpleDateFormat timeFormat = new SimpleDateFormat(TIME_FORMAT);
        String selectedTime = timeFormat.format(calendar.getTime());
        textViewTripTime.setText(selectedTime);
    }

    public class DatePickerFragment extends DialogFragment implements DatePickerDialog.OnDateSetListener {
        @Override
        public Dialog onCreateDialog(Bundle savedInstanceState) {
            final Calendar c = Calendar.getInstance();
            int year = c.get(Calendar.YEAR);
            int month = c.get(Calendar.MONTH);
            int day = c.get(Calendar.DAY_OF_MONTH);
            return new DatePickerDialog(getActivity(), this, year, month, day);
        }

        public void onDateSet(DatePicker view, int year, int month, int day) {
            calendar.set(Calendar.YEAR, year);
            calendar.set(Calendar.MONTH, month);
            calendar.set(Calendar.DAY_OF_MONTH, day);
            updateDate();
        }
    }

    public class TimePickerFragment extends DialogFragment implements TimePickerDialog.OnTimeSetListener {

        @Override
        public Dialog onCreateDialog(Bundle savedInstanceState) {
            // Use the current time as the default values for the picker
            final Calendar c = Calendar.getInstance();
            int hour = c.get(Calendar.HOUR_OF_DAY);
            int minute = c.get(Calendar.MINUTE);

            // Create a new instance of TimePickerDialog and return it
            return new TimePickerDialog(getActivity(), this, hour, minute,
                    DateFormat.is24HourFormat(getActivity()));
        }

        public void onTimeSet(TimePicker view, int hourOfDay, int minute) {
            calendar.set(Calendar.HOUR_OF_DAY, hourOfDay);
            calendar.set(Calendar.MINUTE, minute);
            updateTime();
        }
    }

    // When the user touches somewhere else other than the focusable object, hide the keyboard
    @Override
    public boolean onTouchEvent(MotionEvent event) {
        InputMethodManager imm = (InputMethodManager)getSystemService(Context.
                INPUT_METHOD_SERVICE);
        imm.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(), 0);
        return true;
    }

    public void openTripDetail(View v) {
        startActivity(new Intent(this, RouteActivity.class));
    }

    public void useCurrentPosition(View v){
        if (mGoogleApiClient.isConnected()){
            positionEditText.setText("Current Position");
        } else {
            CharSequence text = "We are not able to get your current position. Please consider " +
                    "giving us location permission and enabling your google play services.";
            int duration = Toast.LENGTH_LONG;
            Toast toast = Toast.makeText(context, text, duration);
            toast.show();
        }
    }

    // Function called when the user clicks on the main search button
    public void sendTravelRequest (View v) {
        String stPosition, edPosition, userId, startTime, endTime, requestTime, priority;
        String startPositionLatitude, startPositionLongitude;
        int selectedId;

        Date now = new Date();
        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.ENGLISH);
        startTime = "null";
        endTime = "null";
        priority = "";
        requestTime = df.format(now);
        userId = ClientAuthentication.getClientId();
        stPosition = positionEditText.getText().toString();
        edPosition = destinationEditText.getText().toString();
        startPositionLatitude = String.valueOf(currentLatitude);
        startPositionLongitude = String.valueOf(currentLongitude);

        selectedId = tripTimeRadioGroup.getCheckedRadioButtonId();

        switch(selectedId){
            case R.id.radiobutton_search_departuretime:
                startTime = df.format(calendar.getTime());
                break;

            case R.id.radiobutton_search_arrivaltime:
                endTime = df.format(calendar.getTime());
                break;
        }

        selectedId = priorityRadioGroup.getCheckedRadioButtonId();

        switch(selectedId){
            case R.id.radiobutton_search_prioritytripdistance:
                priority = "distance";
                break;

            case R.id.radiobutton_search_prioritytriptime:
                priority = "time";
                break;
        }

        if(stPosition != null && !stPosition.trim().isEmpty() && edPosition != null && !edPosition.trim().isEmpty()){
            Storage.clearAll();
            SendTravelRequest asyncTask = new SendTravelRequest();
            asyncTask.delegate = this;
            asyncTask.execute(userId, startTime, endTime, requestTime, stPosition, edPosition, priority,
                    startPositionLatitude, startPositionLongitude);
        }
        else if (stPosition == null || stPosition.trim().isEmpty()) {
            CharSequence text = "Please enter a departure address.";
            int duration = Toast.LENGTH_SHORT;
            Toast toast = Toast.makeText(context, text, duration);
            toast.show();
        }
        else if (edPosition == null || edPosition.trim().isEmpty()) {
            CharSequence text = "Please enter a destination address.";
            int duration = Toast.LENGTH_SHORT;
            Toast toast = Toast.makeText(context, text, duration);
            toast.show();
        }
    }

    public void processFinish(ArrayList<FullTrip> searchResults){
        if (searchResults.isEmpty()){
            CharSequence text = "Could not find any trips matching your criteria.";
            int duration = Toast.LENGTH_SHORT;
            Toast toast = Toast.makeText(context, text, duration);
            toast.show();
        }
        adapter = new SearchRecyclerViewAdapter(searchResults);
        recyclerView.setAdapter(adapter);
    }

    @Override
    protected void onResume() {
        super.onResume();

        if (checkPlayServices()){
            if (!mGoogleApiClient.isConnected()) {
                if (Build.VERSION.SDK_INT >= 23){
                    checkForPermission();
                } else {
                    mGoogleApiClient.connect();
                }
            }
        } else {
            CharSequence text = "If you don't have google play services enabled then we can't use " +
                    "your current location to search for suitable bus trips.";
            int duration = Toast.LENGTH_LONG;
            Toast toast = Toast.makeText(context, text, duration);
            toast.show();
        }

        if (getIntent().hasExtra("destination")){
            destinationEditText.setText(getIntent().getStringExtra("destination"));
        }

        searchResults = Storage.getSearchResults();
        adapter = new SearchRecyclerViewAdapter(searchResults);
        recyclerView.setAdapter(adapter);
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (mGoogleApiClient.isConnected()) {
            LocationServices.FusedLocationApi.removeLocationUpdates(mGoogleApiClient, this);
            mGoogleApiClient.disconnect();
        }
    }

    @Override
    public void onConnected(Bundle bundle) {
        Location location = LocationServices.FusedLocationApi.getLastLocation(mGoogleApiClient);

        if (location == null) {
            LocationServices.FusedLocationApi.requestLocationUpdates(mGoogleApiClient, mLocationRequest, this);
        } else {
            handleNewLocation(location);
        }
    }

    @Override
    public void onConnectionSuspended(int i) {

    }

    @Override
    public void onConnectionFailed(ConnectionResult connectionResult) {
        Log.d("oops", "Connection failed with error code: " + Integer.toString(connectionResult.getErrorCode()));
    }

    @Override
    public void onLocationChanged(Location location) {
        handleNewLocation(location);
    }

    private boolean checkPlayServices() {
        GoogleApiAvailability apiAvailability = GoogleApiAvailability.getInstance();
        int resultCode = apiAvailability.isGooglePlayServicesAvailable(this);
        if (resultCode != ConnectionResult.SUCCESS) {
            if (apiAvailability.isUserResolvableError(resultCode)) {
                apiAvailability.getErrorDialog(this, resultCode, PLAY_SERVICES_RESOLUTION_REQUEST).show();
            }
            return false;
        }
        return true;
    }
}
