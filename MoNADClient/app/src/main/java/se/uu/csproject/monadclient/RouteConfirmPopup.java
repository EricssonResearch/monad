package se.uu.csproject.monadclient;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class RouteConfirmPopup extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.popup_route_confirm);

        DisplayMetrics dm = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(dm);
        int width = dm.widthPixels;
        int height = dm.heightPixels;
        getWindow().setLayout((int) (width * .9), (int) (height * .40));

        TextView tvCancel = (TextView) findViewById(R.id.tv_link_trip_back);
        tvCancel.setOnClickListener(new View.OnClickListener() {
            public void onClick(View vw) {
                startActivity(new Intent(RouteConfirmPopup.this, RouteActivity.class));
            }
        });

        Button btn_trip_confirm = (Button) findViewById(R.id.button_trip_confirm);
        btn_trip_confirm.setOnClickListener(new View.OnClickListener() {
            public void onClick(View vw) {
                startActivity(new Intent(RouteConfirmPopup.this, RouteSuccessActivity.class));
            }
        });

    }
}
