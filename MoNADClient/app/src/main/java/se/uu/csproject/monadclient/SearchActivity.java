package se.uu.csproject.monadclient;

import android.Manifest;
import android.app.DatePickerDialog;
import android.app.Dialog;
import android.app.DialogFragment;
import android.app.TimePickerDialog;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.os.Build;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.text.Selection;
import android.text.format.DateFormat;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;
import android.view.inputmethod.InputMethodManager;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.DatePicker;
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

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
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
    DialogFragment dateFragment, timeFragment;
    private RadioGroup tripTimeRadioGroup, priorityRadioGroup;
    private AutoCompleteTextView positionEditText, destinationEditText;
    private GoogleApiClient mGoogleApiClient;
    private LocationRequest mLocationRequest;
    private double currentLatitude, currentLongitude;
    private Context context;
    private ArrayList<FullTrip> searchResults;
    private SearchRecyclerViewAdapter adapter;
    private LinearLayoutManager linearLayoutManager;
    private RecyclerView recyclerView;
    private Toolbar toolbar;

    private static final int PLAY_SERVICES_RESOLUTION_REQUEST = 9000;
    private final int MY_PERMISSIONS_REQUEST = 123;

    public Calendar calendar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search);
        toolbar = (Toolbar) findViewById(R.id.actionToolBar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setHomeButtonEnabled(true);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        getSupportActionBar().setHomeAsUpIndicator(R.drawable.ic_home_white_24dp);


        context = getApplicationContext();
        textViewTripDate = (TextView) findViewById(R.id.textview_search_tripdate);
        textViewTripTime = (TextView) findViewById(R.id.textview_search_triptime);
        calendar = Calendar.getInstance();
        updateDate();
        updateTime();

        tripTimeRadioGroup = (RadioGroup) findViewById(R.id.radiogroup_search_triptime);
        priorityRadioGroup = (RadioGroup) findViewById(R.id.radiogroup_search_priority);
        positionEditText = (AutoCompleteTextView) findViewById(R.id.edittext_search_position);
        destinationEditText = (AutoCompleteTextView) findViewById(R.id.edittext_search_destination);

        recyclerView = (RecyclerView) findViewById(R.id.recycler_view_search);
        linearLayoutManager = new LinearLayoutManager(getApplicationContext());
        recyclerView.setLayoutManager(linearLayoutManager);

        currentLatitude = 0;
        currentLongitude = 0;

        buildGoogleApiClient();
        initializeLocationRequest();
        String[] addresses = getAddressesFromFileAsset();

        if (addresses != null){
            ArrayAdapter<String> adapterString =
                    new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, addresses);
            positionEditText.setAdapter(adapterString);
            destinationEditText.setAdapter(adapterString);
        }

        // Hide the keyboard when launching this activity
        this.getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_HIDDEN);
    }

    public String[] getAddressesFromFileAsset(){
        String[] addresses = null;
        ArrayList<String> addressesList = new ArrayList<>();
        String line;

        try{
            BufferedReader reader = new BufferedReader(new InputStreamReader(getAssets().open("addresses.txt")));
            while ((line = reader.readLine()) != null) {
                addressesList.add(line);
            }
            addresses = new String[addressesList.size()];
            addresses = addressesList.toArray(addresses);
        }
        catch (IOException e) {
            Log.d("oops", e.toString());
        }

        return addresses;
    }

    // Checks if the user has given location permission and asks for it if he hasn't
    private void checkForPermission(){
        if (ContextCompat.checkSelfPermission(SearchActivity.this, Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED){
            ActivityCompat.requestPermissions(SearchActivity.this,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, MY_PERMISSIONS_REQUEST);
        } else {
            mGoogleApiClient.connect();
        }
    }

    // Checks the result of the permission asked of the user
    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        switch (requestCode) {
            case MY_PERMISSIONS_REQUEST: {
                // Permission granted!
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    mGoogleApiClient.connect();
                } else {
                    // Permission denied, boo! Pester him until he changes his mind
                    CharSequence text = getString(R.string.java_locationpermissionwarning);
                    Toast toast = Toast.makeText(context, text, Toast.LENGTH_LONG);
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
            DatePickerDialog dialog = new DatePickerDialog(getActivity(), this, year, month, day);
            dialog.getDatePicker().setMinDate(new Date().getTime() - 1000);
            return dialog;
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

    // Called when the user clicks on the pinpoint icon next to the departure address field
    public void useCurrentPosition(View v){
        if (mGoogleApiClient.isConnected()){
            positionEditText.setText(getString(R.string.java_search_currentposition));
            Selection.setSelection(positionEditText.getText(), positionEditText.length());
        } else {
            CharSequence text = getString(R.string.java_search_locationfailed);
            Toast toast = Toast.makeText(context, text, Toast.LENGTH_LONG);
            toast.show();
        }
    }

    // Called when the user clicks on the main search button
    public void sendTravelRequest (View v) {
        String stPosition, edPosition, userId, startTime, endTime, requestTime, priority;
        String startPositionLatitude, startPositionLongitude;
        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.ENGLISH);
        Date now = new Date();
        int selectedId;

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
            Storage.clearSearchResults();
            SendTravelRequest asyncTask = new SendTravelRequest();
            asyncTask.delegate = this;
            asyncTask.execute(userId, startTime, endTime, requestTime, stPosition, edPosition, priority,
                    startPositionLatitude, startPositionLongitude);
        }
        else if (stPosition == null || stPosition.trim().isEmpty()) {
            CharSequence text = getString(R.string.java_search_enterdeparture);
            Toast toast = Toast.makeText(context, text, Toast.LENGTH_SHORT);
            toast.show();
        }
        else if (edPosition == null || edPosition.trim().isEmpty()) {
            CharSequence text = getString(R.string.java_search_enterdestination);
            Toast toast = Toast.makeText(context, text, Toast.LENGTH_SHORT);
            toast.show();
        }
    }

    // Deals with the response by the server
    public void processFinish(ArrayList<FullTrip> searchResults){
        if (searchResults.isEmpty()){
            CharSequence text = getString(R.string.java_search_emptysearch);
            Toast toast = Toast.makeText(context, text, Toast.LENGTH_SHORT);
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
            CharSequence text = getString(R.string.java_googleplaywarning);
            Toast toast = Toast.makeText(context, text, Toast.LENGTH_LONG);
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

    // Checks if the user has google play services enabled
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
