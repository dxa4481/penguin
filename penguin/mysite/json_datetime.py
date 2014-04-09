import datetime



dthandler = lambda obj: (
        obj.isoformat()                                                                                                                                                              
        if isinstance(obj, datetime.datetime)                                                                                                                                        
        or isinstance(obj, datetime.date)                                                                                                                                            
        else None)
