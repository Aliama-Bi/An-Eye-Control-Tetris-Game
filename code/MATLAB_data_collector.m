% Script reads data from BackyardBrain's Arduino SpikerShield
% https://backyardbrains.com/products/heartAndBrainSpikerShieldBundle
% script produces data in "result" variable
clear all
close all
delete(instrfindall);

port_number = 7; % change this depending on what is the number in "device manager" 

%-------------------------------------------------------------------------------
% Parameters
%-------------------------------------------------------------------------------

total_time = 100; % code will stop after this amount of time in seconds [[1 s = 20000 buffer size]]

max_time = 10; % time plotted in window [s]

%-------------------------------------------------------------------------------
% Initialize import data stream
%-------------------------------------------------------------------------------

inputBufferSize = 1000;   % Bufffer Size - in the range 1000-20000
% e.g. inputBufferSize = 20000 means it waits 1 second before plotting

s = InitializePortInput(inputBufferSize,port_number);

%-------------------------------------------------------------------------------
% Record and plot data
%-------------------------------------------------------------------------------
figure('color','w');
xlabel('Time (s)')
ylabel('Input signal (arb)')
data = [];

N_loops = 20000/s.InputBufferSize*total_time;

T_acquire = s.InputBufferSize/20000;    % length of time that data is acquired for 
N_max_loops = max_time/T_acquire;       %total number of loops to cover desire time window

% Store the number of data collection iterations to wait before analysing
% data
n_wait =0;

% Store the current possible signal
possible_signal = 'none';

% Store the total possible detections made
totPossibleDetections =0;

% Sampling Rate
Fs = 10000;

% Empirically determined peak filtering values
trough_threshold = 0.94;
peak_threshold = 1.07;
up_threshold = 0.7;

for i = 1:N_loops 
    draw_peaks = false;
    % take enough data to cover the first time window

    % read and process data first
    data = fread(s)';
    data_temp = process_data(data);
    % start loops
    if i <= N_max_loops
        if i==1
            data_actual = data_temp;
        else
            data_actual = [data_temp data_actual]; % the result stream will be in data variable            
        end
        
        % Calculate time array
        
        t = min(i,N_max_loops)*s.InputBufferSize/20000*linspace(0,1,length(data_actual));
        
        % Plot the calibration data
        drawnow;
        plot(t,data_actual)
        xlabel('time (s)')
        xlim([0,max_time])
          

    else % When the first 10 seconds of calibration are over
        
        % Calculate the noise level as soon as calibration time elapses
        if i==N_max_loops+1
            noise_level = mean(data_actual);
        end
        
        % continue adding data to the time window after window is finished
        data_actual = circshift(data_actual,[0 length(data_temp)]);
        data_actual(1:length(data_temp)) = data_temp';
        
        % Calculate time array
        t = min(i,N_max_loops)*s.InputBufferSize/20000*linspace(0,1,length(data_actual));
        
        % Normalise data and calculate size of array
        
        %dataNorm = data_actual-noise_level;
        dataNorm = data_actual;
        N = size(dataNorm,1);
        dF = Fs/N; % Frequency step
        f = (-Fs/2:dF:Fs/2-dF)'; % Frequency vector
        
        % Apply FFT filter
        
        lower_freq = 1;
        BPF = (lower_freq < abs(f)); % define band pass filter
        spectrum = fftshift(fft(dataNorm))/N; % Apply fft to characterise frequencies
        spectrum = BPF.*spectrum; % Cut out required frequencies
        % Use band passed spectrum to filter original data.
        fft_filtered = ifft(ifftshift(spectrum),'symmetric')*N;
        
        % Apply Butter filter
        
        cut_f = 5; %Hz
        [b,a] = butter(5,cut_f/(Fs/2)); % Set up parameters for filter.
        doubleFiltered = (filtfilt(b,a,double(fft_filtered')));
        
        % if n_wait=0 , analyse data. If n_wait !=0 , just collect data.
        
        if n_wait==0 % analyse data
            % if possible_signal==none , try to find possible signal by
            % looking at peaks. if possible_signal=='up','down', or 'blik'
            % package the collected data and store in file. 
            
            if strcmp(possible_signal,'none') % Find peaks in data
                search_time = 0.2; % most recent seconds over which to look for events
                % Find troughs
                [PKS,LOCS] = findpeaks(-1.*doubleFiltered(t<=search_time)); % search in most recent search_time sec
                conditionTrough = PKS>=-trough_threshold*noise_level; % boolean array to filter for troughs
                locsTrough = LOCS(conditionTrough); % locations of troughs
                troughs = PKS(conditionTrough); % value of troughs
                % Find peaks
                [PKS,LOCS] = findpeaks(doubleFiltered(t<=search_time)); % search in most recent search_time sec
                conditionPeak = PKS>=peak_threshold*noise_level; % boolean array to filter for peaks
                locsPeak = LOCS(conditionPeak); % locations of peaks
                peaks= PKS(conditionPeak); % value of peaks
                
                
                if (~isempty(locsTrough))||(~isempty(locsPeak))
                    disp('POSSIBLE SIGNAL DETECTED')
                    possible_signal = 'up,down or blink';
                    totPossibleDetections = totPossibleDetections+1;
                    t_wait = 1.5; % s to collect enough data around possible event.
                    n_wait = round(t_wait/T_acquire)+1; % convert waiting time into number of loop steps.
                
                end
                
            else  % Store collected time window in file
 
                % Query the data since the possible event was triggered.
                possibleEventData = doubleFiltered(t<=t_wait+search_time+0.4)-noise_level;
                possibleEventData = int16(possibleEventData); % suitable save format
                filename = strcat('wave_file_',string(totPossibleDetections),'.wav');
                audiowrite(filename,possibleEventData,Fs);
                
                % Reset values and let it equilibrate for 0.2 sec
                possible_signal = 'none';
                n_wait = round(0.2/T_acquire)+1;
                  
            end
        end
        
        % Display filtered wave data
        drawnow;
        plot(t,doubleFiltered)
        xlabel('time (s)')
        xlim([0,max_time])
        %ylim([-500 500])
             
    end
    
    % Update waiting time to analysis
    if n_wait>0
        n_wait = n_wait-1;
    end
end

%{
finalData = int16(data_actual); % suitable save format
filename = strcat('wave_file_for_flowchart_plots.wav');
audiowrite(filename,finalData,Fs);
%}

for j=totPossibleDetections:-1:1
    file_name = strcat('wave_file_',string(j),'.wav');
    delete(file_name)
end



