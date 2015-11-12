package se.uu.csproject.monadclient;

import android.content.Context;
import android.content.Intent;
import android.os.CountDownTimer;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

import se.uu.csproject.monadclient.recyclerviews.FullTrip;

import static java.lang.Math.floor;

public class TripCancelPopup extends AppCompatActivity implements AsyncResponseString{
    private TextView startBusStop, endBusStop, startTime, endTime, date, countdown;
    private ImageView clockIcon;
    private FullTrip trip;
    private Context context;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.popup_trip_cancel);

        startBusStop = (TextView) findViewById(R.id.label_startbusstop);
        endBusStop = (TextView) findViewById(R.id.label_endbusstop);
        startTime = (TextView) findViewById(R.id.label_starttime);
        endTime = (TextView) findViewById(R.id.label_endtime);
        date = (TextView) findViewById(R.id.label_date);
        countdown = (TextView) findViewById(R.id.label_countdown);
        clockIcon = (ImageView) findViewById(R.id.icon_clock);
        context = getApplicationContext();

        Bundle b = getIntent().getExtras();
        trip = b.getParcelable("selectedTrip");
        startBusStop.setText(trip.getStartBusStop());
        endBusStop.setText(trip.getEndBusStop());
        startTime.setText(formatTime(trip.getStartTime()));
        endTime.setText(formatTime(trip.getEndTime()));
//        if(trip.isToday()){
//            date.setText("TODAY");
//        }
//        final long MILLISECONDS_TO_DEPARTURE = trip.getTimeToDeparture();
//        countdown.setText(String.valueOf(MILLISECONDS_TO_DEPARTURE));
//
//        final int MILLISECONDS = b.getInt("MILLISECONDS");
//        CountDownTimer timer = new CountDownTimer(MILLISECONDS_TO_DEPARTURE, MILLISECONDS) {
//            @Override
//            public void onTick(long millisUntilFinished) {
//                countdown.setText(formatCoundownText(millisUntilFinished));
//                if (millisUntilFinished < 1800000) {
//                    countdown.setTextColor(ContextCompat.getColor(countdown.getContext(), R.color.warnColor));
//                    date.setTextColor(ContextCompat.getColor(date.getContext(), R.color.warnColor));
//                    clockIcon.setVisibility(View.VISIBLE);
//                }
//            }
//
//            @Override
//            public void onFinish() {
//                countdown.setText("Trip in Progress");
//                countdown.setTextColor(ContextCompat.getColor(countdown.getContext(), R.color.green));
//                date.setTextColor(ContextCompat.getColor(countdown.getContext(), R.color.green));
//                clockIcon.setVisibility(View.INVISIBLE);
//                //clockIcon.setColorFilter(ContextCompat.getColor(clockIcon.getContext(), R.color.green));
//            }
//        }.start();


        final int MILLISECONDS = 1000;
        if(trip.isInProgress()){
            formatAsInProgress();
        }
        else{
            if(trip.isToday()){
                date.setText(getString(R.string.java_today));
                date.setTextColor(ContextCompat.getColor(getApplicationContext(), R.color.warnColor));
            }
            else {
                date.setText(formatDate(trip.getStartTime()));
            }

            final long MILLISECONDS_TO_DEPARTURE = trip.getTimeToDeparture();
            countdown.setText(formatCountdownText(MILLISECONDS_TO_DEPARTURE));

            CountDownTimer timer = new CountDownTimer(MILLISECONDS_TO_DEPARTURE, MILLISECONDS) {
                @Override
                public void onTick(long millisUntilFinished) {
                    countdown.setText(formatCountdownText(millisUntilFinished));
                    //change value to 30min (30*60*1000 = 1 800 000ms)
                    if (millisUntilFinished < 1800000) {
                        countdown.setTextColor(ContextCompat.getColor(getApplicationContext(), R.color.warnColor));
                        clockIcon.setVisibility(View.VISIBLE);
                    }
                }

                @Override
                public void onFinish() {
                    formatAsInProgress();
                }
            }.start();
        }

        //////////////////////////////////////////
        DisplayMetrics dm = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(dm);
        int width = dm.widthPixels;
        int height = dm.heightPixels;
        getWindow().setLayout((int) (width * .9), (int) (height * .38));
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    // Cancel the trip
    public void dropTrip(View view) {
        String userTripId = trip.getId();
        SendBookingCancelRequest asyncTask = new SendBookingCancelRequest();
        asyncTask.delegate = this;
        asyncTask.execute(userTripId);
    }

    // Deal with the response from the server after the user cancels the trip
    public void processFinish(String response){
        Toast toast = Toast.makeText(context, response, Toast.LENGTH_SHORT);
        toast.show();
        startActivity(new Intent(this, TripsActivity.class));
        finish();
    }

    public void backButtonClick(View view) {
        finish();
    }

    private String formatCountdownText(long millisecondsTime){
        DecimalFormat formatter = new DecimalFormat("00");
        String hours = formatter.format( floor(millisecondsTime / (1000 * 60 * 60)) );
        millisecondsTime %= (1000*60*60);
        String minutes = formatter.format( floor(millisecondsTime / (1000*60)) );
        millisecondsTime %= (1000*60);
        String seconds = formatter.format( floor(millisecondsTime / 1000) );
        return hours + ":" + minutes + ":" + seconds;
    }

    private String formatTime(Date date){
        Calendar calendar = Calendar.getInstance();
        calendar.setTime(date);
        SimpleDateFormat timeFormat = new SimpleDateFormat("HH:mm");
        return timeFormat.format(calendar.getTime());
    }

    private String formatDate(Date date){
        Calendar calendar = Calendar.getInstance();
        calendar.setTime(date);
        SimpleDateFormat dateFormat = new SimpleDateFormat("EEE dd MMM.");
        return dateFormat.format(calendar.getTime());
    }

    private void formatAsInProgress() {
        date.setText(getString(R.string.java_today));
        countdown.setText(getString(R.string.java_tripinprogress));
        countdown.setTextColor(ContextCompat.getColor(getApplicationContext(), R.color.green));
        date.setTextColor(ContextCompat.getColor(getApplicationContext(), R.color.green));
        clockIcon.setVisibility(View.INVISIBLE);
    }
}
