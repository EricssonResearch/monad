package se.uu.csproject.monadclient.activities;

import android.app.DatePickerDialog;
import android.app.Dialog;
import android.app.DialogFragment;
import android.app.TimePickerDialog;
import android.content.Context;
import android.os.Bundle;
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

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

import se.uu.csproject.monadclient.ClientAuthentication;
import se.uu.csproject.monadclient.R;
import se.uu.csproject.monadclient.interfaces.AsyncResponse;
import se.uu.csproject.monadclient.storage.FullTrip;
import se.uu.csproject.monadclient.recyclerviews.SearchRecyclerViewAdapter;
import se.uu.csproject.monadclient.storage.Storage;
import se.uu.csproject.monadclient.serverinteractions.SendTravelRequest;

public class SearchActivity extends MenuedActivity implements AsyncResponse {
    private TextView textViewTripDate, textViewTripTime;
    DialogFragment dateFragment, timeFragment;
    private RadioGroup tripTimeRadioGroup, priorityRadioGroup;
    private AutoCompleteTextView positionEditText, destinationEditText;
    private Context context;
    private ArrayList<FullTrip> searchResults;
    private SearchRecyclerViewAdapter adapter;
    private LinearLayoutManager linearLayoutManager;
    private RecyclerView recyclerView;
    private Toolbar toolbar;

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
        InputMethodManager imm = (InputMethodManager)getSystemService(INPUT_METHOD_SERVICE);
        imm.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(), 0);
        return true;
    }

    // Called when the user clicks on the pinpoint icon next to the departure address field
    public void useCurrentPosition(View v){
        if (Storage.getLatitude() != 0.0 && Storage.getLongitude() != 0.0){
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
        startPositionLatitude = String.valueOf(Storage.getLatitude());
        startPositionLongitude = String.valueOf(Storage.getLongitude());

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
            Storage.clearSearchResults();
        }
        adapter = new SearchRecyclerViewAdapter(searchResults);
        recyclerView.setAdapter(adapter);
    }

    @Override
    protected void onResume() {
        super.onResume();

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
    }
}
