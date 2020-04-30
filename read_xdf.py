from xdf_parser import load_xdf

def read_xdf(path):
    ''' Reads .xdf files

    Input: 
        path:: string
            path to .xdf file
    Output:
        result:: dict
            dictionary containing the most relevant information
        data:: dict
            dictionary containing all the data directly
            from xdf_parser
    '''

    data = load_xdf(path)
    result = {}
    for stream in data[0]:
        stream_name = stream['info']['name'][0]
        result[stream_name] = {}

        # Info
        result[stream_name]['fs'] = int(stream['info']['nominal_srate'][0])
        result[stream_name]['type'] = stream['info']['type'][0].lower()
        result[stream_name]['first_ts'] = float(stream['footer']['info']['first_timestamp'][0])
        result[stream_name]['last_ts'] = float(stream['footer']['info']['last_timestamp'][0])
        result[stream_name]['total_stream_time'] = result[stream_name]['last_ts'] - result[stream_name]['first_ts']
        result[stream_name]['sample_count'] = int(stream['footer']['info']['sample_count'][0])
        result[stream_name]['data_type'] = stream['info']['channel_format'][0]
        result[stream_name]['hostname'] = stream['info']['hostname'][0]

        # Data
        result[stream_name]['data'] = stream['time_series']
        result[stream_name]['ts'] = stream['time_stamps']

        # Manually added stream description
        if stream['info']['desc'][0] is not None:
            for desc in stream['info']['desc']:
                # TODO: differentiate between channel types (e.g. gtec has eeg and accelerometer channels (and more))
                if 'channels' in desc.keys():
                    result[stream_name]['channel_names'] = [ch['label'][0] for ch in desc['channels'][0]['channel']]
                if 'manufacturer' in desc.keys():
                    result[stream_name]['manufacturer'] = desc['manufacturer'][0]

    return result, data


path = r'C:\Users\p70066129\Data\BCI\Grasp\raw/'
filename = r'grasp_p4_20200221.xdf'
result, data = read_xdf(path+filename)

print('done')