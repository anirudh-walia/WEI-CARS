pragma solidity 0.4.25;

contract carcontract{
    
    address adds;
	string carname;
	string carno;
	int basecharge;
	int chargeperkm;
    int maxspeed;
    int penperms;
    string pickup;
    string special;
    
    address radds;
    string dateandtime;
    int houurs;
    string haash;
    
    struct trx{
        string hashh;
        string date_and_time;
        int hourss;
    }
    
    struct carContra{
        string car;
        string number;
        int charge_base;
        int charge_km;
        int max_speed;
        int pen_perms;
        string pickup_place;
        string speciall;
    }
        
	mapping(address=>carContra) mapcarContra;
	address[] public caraccs;
	
        
    function saveContract(address _address, string memory _carname, 
                          string memory _carno, int _basecharge, int _chargeperkm,
                          int _maxspeed, int _penperms, string memory _pickup, 
                          string memory _special)  public{
        
        adds = _address;
    	carname = _carname;
    	carno = _carno;
    	basecharge = _basecharge;
    	chargeperkm = _chargeperkm;
    	maxspeed = _maxspeed;
        penperms = _penperms;
        pickup = _pickup;
        special = _special;
    	
    	carContra storage car_array_2 = mapcarContra[adds];
    	
    	car_array_2.car = carname;
    	car_array_2.number = carno;
    	car_array_2.charge_base = basecharge;
    	car_array_2.charge_km = chargeperkm;
    	car_array_2.max_speed = maxspeed;
    	car_array_2.pen_perms = penperms;
    	car_array_2.pickup_place = pickup;
    	car_array_2.speciall = special;
    	
        caraccs.push(adds) -1;
    	
    }
    
    function getContract(address) view public returns (string , string, int , int ,
                          int , int, string , string ){
        
        return(mapcarContra[adds].car, mapcarContra[adds].number, 
               mapcarContra[adds].charge_base, mapcarContra[adds].charge_km, 
               mapcarContra[adds].max_speed, mapcarContra[adds].pen_perms, 
               mapcarContra[adds].pickup_place, mapcarContra[adds].speciall);
        
    }
    
    mapping(address=>trx) trx_arr;
    address[] public trxaccs;
    
    function taketrx(address _addresss, string _haash, 
                     string _dateandtime, int _hours) public {
        
        radds = _addresss;
        haash = _haash;
        dateandtime = _dateandtime;
        houurs = _hours;
        
        trx storage trx_2 = trx_arr[radds];
        
        trx_2.hashh = haash;
        trx_2.date_and_time = dateandtime;
        trx_2.hourss = houurs;
        
        trxaccs.push(radds) -1;
    }
    
    function givetrx(address) view public returns(string, string, int){
        
        return(trx_arr[radds].date_and_time, trx_arr[radds].hashh, 
               trx_arr[radds].hourss);
        
    }
    
}




