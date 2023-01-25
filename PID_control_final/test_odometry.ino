void odometry() {
  //6.7*3.141592*(rpm/60)
  dltDistL = 20*3.141592*(-d_e1cnt / 1320.);
  dltDistR = 20*3.141592*(-d_e2cnt / 1320.);
  dltTheta = (dltDistR-dltDistL)/60;
  //Serial.println(dltTheta);

  now_theta += dltTheta; 
  now_x += ( ((dltDistL + dltDistR)/2) * cos(now_theta + (dltDistR-dltDistL)/2L));
  now_y += ( ((dltDistL + dltDistR)/2) * sin(now_theta + (dltDistR-dltDistL)/2L));

}

void go(float m1, float m2){
  m1_ref_spd = -m1;
  m2_ref_spd = m2;
  ComputePID();
}
