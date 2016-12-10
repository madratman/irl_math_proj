mmp = [0.06513
0.05521
0.043994
0.042715
-0.0094772
0.058692
0.053302
0.052339
0.067768
0.0026747
0.056005
0.054976
0.053353
0.069732
0.003524
0.056014
0.054323
0.053996
0.065693
0.0039981
0.05389
0.054667
0.055777
0.054926
0.0023227
0.16433
];

maxent = [0.38188
0.316585
0.404126
0.00842033
0.0278719
0.381659
0.33031
0.38756
0.146917
0.278746
0.425011
0.295897
0.388504
0.359881
0.375999
0.374703
0.363185
0.35902
0.465574
0.399319
0.346569
0.411175
0.342861
0.564461
0.409718
0.305364];

hold on;
plot(1:26, mmp,'LineWidth', 3);
plot(1:26, maxent,'LineWidth', 3);
legend('mmp','maxent','Location', 'northwest')

one_hot_indices = [1 2 3; 6 7 8; 11 12 13; 16 17 18; 21 22 23];
one_hot_indices = one_hot_indices';
one_hot_indices = one_hot_indices(:);
dist_indices = [4 5 9 10 14 15 19 20 24 25];
bias = [26];

plot(one_hot_indices,mmp(one_hot_indices), 'o', 'MarkerSize', 10, 'LineWidth', 2);	
plot(dist_indices,mmp(dist_indices), '*', 'MarkerSize', 10, 'LineWidth', 2);	
plot(bias,mmp(bias), '^', 'MarkerSize', 10, 'LineWidth', 2);	

plot(one_hot_indices,maxent(one_hot_indices), 'o', 'MarkerSize', 7.5, 'LineWidth', 2);	
plot(dist_indices,maxent(dist_indices), 'x', 'MarkerSize', 7.5, 'LineWidth', 2);	
plot(bias,maxent(bias), '^', 'MarkerSize', 7.5, 'LineWidth', 2);	

% scatter(1:26, mmp, '*')
% scatter(1:26, maxent, '*')
