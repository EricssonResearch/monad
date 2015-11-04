package se.uu.csproject.monadclient;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextView;

import java.util.Calendar;

public class RouteConfirmPopup extends AppCompatActivity {

    private TextView busIdView;
    private TextView startTimeView;
    private TextView endTimeView;
    private TextView stPositionView;
    private TextView edPositionView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.popup_route_confirm);

        DisplayMetrics dm = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(dm);
        int width = dm.widthPixels;
        int height = dm.heightPixels;
        getWindow().setLayout((int) (width * .9), (int) (height * .40));

        busIdView = (TextView) findViewById(R.id.businfo);
        startTimeView = (TextView) findViewById(R.id.departtime);
        endTimeView = (TextView) findViewById(R.id.arrivetime);
        stPositionView = (TextView) findViewById(R.id.departname);
        edPositionView = (TextView) findViewById(R.id.arrivename);

        ImageButton cancel = (ImageButton)findViewById(R.id.cancelbutton);
        cancel.setOnClickListener(new View.OnClickListener() {
            public void onClick(View vw) {
                //return to the previous activity instead of start a new one
                finish();
            }


        });
    }

    public void confirmTrip(View view){
        String busId, busIdText[], startTime, startTimeText, endTime, endTimeText, stPosition, edPosition, userId;
        int currentYear, currentMonth, currentDay;
        Calendar rightNow = Calendar.getInstance();

        currentYear = rightNow.get(Calendar.YEAR);
        currentMonth = rightNow.get(Calendar.MONTH);
        // Genius design choice: months are numbered 0-11
        currentMonth++;
        currentDay = rightNow.get(Calendar.DAY_OF_MONTH);

        busIdText = ( busIdView.getText().toString() ).split("\\s+");
        busId = busIdText[1];
        userId = ClientAuthentication.getClientId();
        startTimeText = startTimeView.getText().toString();
        startTime = currentYear + " " + currentMonth + " " + currentDay + " " + startTimeText;
        endTimeText = endTimeView.getText().toString();
        endTime = currentYear + " " + currentMonth + " " + currentDay + " " + endTimeText;
        stPosition = stPositionView.getText().toString();
        edPosition = edPositionView.getText().toString();

        //new SendBookingRequest().execute(busId, userId, startTime, endTime, stPosition, edPosition);

        startActivity(new Intent(RouteConfirmPopup.this, RouteSuccessActivity.class));
        finish();
    }
}
