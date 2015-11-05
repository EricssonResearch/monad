package se.uu.csproject.monadclient;

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

import java.text.DecimalFormat;
import java.util.Calendar;
import java.util.Date;

import se.uu.csproject.monadclient.recyclerviews.FullTrip;
import se.uu.csproject.monadclient.recyclerviews.Trip;

import static java.lang.Math.floor;

public class TripCancelPopup extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.popup_trip_cancel);

        TextView startBusStop = (TextView) findViewById(R.id.label_startbusstop);
        TextView endBusStop = (TextView) findViewById(R.id.label_endbusstop);
        TextView startTime = (TextView) findViewById(R.id.label_starttime);
        TextView endTime = (TextView) findViewById(R.id.label_endtime);
        final TextView date = (TextView) findViewById(R.id.label_date);
        final TextView countdown = (TextView) findViewById(R.id.label_countdown);
        final ImageView clockIcon = (ImageView) findViewById(R.id.icon_clock);

        Bundle b = getIntent().getExtras();
        final FullTrip trip = b.getParcelable("selectedTrip");
        startBusStop.setText(trip.getStartBusStop());
        endBusStop.setText(trip.getEndBusStop());
        startTime.setText(formatTime(trip.getStartTime()));
        endTime.setText(formatTime(trip.getEndTime()));
        if(trip.isToday()){
            date.setText("TODAY");
        }
        final long MILLISECONDS_TO_DEPARTURE = trip.getTimeToDeparture();
        countdown.setText(String.valueOf(MILLISECONDS_TO_DEPARTURE));

        final int MILLISECONDS = b.getInt("MILLISECONDS");
        CountDownTimer timer = new CountDownTimer(MILLISECONDS_TO_DEPARTURE, MILLISECONDS) {
            @Override
            public void onTick(long millisUntilFinished) {
                countdown.setText(formatCoundownText(millisUntilFinished));
                if (millisUntilFinished < 10000) {
                    countdown.setTextColor(ContextCompat.getColor(countdown.getContext(), R.color.warnColor));
                    date.setTextColor(ContextCompat.getColor(date.getContext(), R.color.warnColor));
                    clockIcon.setVisibility(View.VISIBLE);
                }
            }

            @Override
            public void onFinish() {
                countdown.setText("Trip in Progress");
                countdown.setTextColor(ContextCompat.getColor(countdown.getContext(), R.color.green));
                date.setTextColor(ContextCompat.getColor(countdown.getContext(), R.color.green));
                clockIcon.setVisibility(View.INVISIBLE);
                //clockIcon.setColorFilter(ContextCompat.getColor(clockIcon.getContext(), R.color.green));
            }
        }.start();

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
    //TODO Stavros: remove trip from user's schedule if the confirm button is clicked
    public void dropTrip(View view) {
        //new SendBookingCancelRequest().execute(objectId);
        //startActivity(new Intent(this, MainActivity.class));
        finish();
    }

    public void backButtonClick(View view) {
        finish();
    }

    private String formatCoundownText(long millisecondsTime){
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
        return calendar.HOUR_OF_DAY + ":" + calendar.MINUTE;
    }
}
