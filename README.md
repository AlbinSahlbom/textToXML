# textToXML

This application will take a file with line based information and convert it to corresponding XML format.

Line based file format:  
P|first name|last name  
T|mobile phone number|landline number  
A|street|city|zip code  
F|name|born  

P can be followed by T, A and F  
F can be followed by T and A  

Example:

P|Carl Gustaf|Bernadotte  
T|0768-101801|08-101801  
A|Drottningholms slott|Stockholm|10001  
F|Victoria|1977  
A|Haga Slott|Stockholm|10002  
F|Carl Philip|1979  
T|0768-101802|08-101802  
P|Barack|Obama  
A|1600 Pennsylvania Avenue|Washington, D.C  

This example will produce XML in this format:
```xml
<people>
  <person>
    <firstname>Carl Gustaf</firstname>
    <lastname>Bernadotte</lastname>
    <address>
      <street>Drottningholms slott</street>
      <city>Stockholm</city>
      <zip>10001</zip>
     </address>
    <phone>
      <mobile>0768-101801</mobile>
      <landline>08-101801</landline>
    </phone>
    <family>
      <name>Victoria</name>
      <born>1977</born>
      <address>
        <street>Haga Slott</street>
        <city>Stockholm</city>
        <zip>10002</zip>
      </address>
    </family>
    <family>
      <name>Carl Philip</name>
      <born>1979</born>
      <phone>
        <mobile>0768-101802</mobile>
        <landline>08-101802</landline>
      </phone>
    </family>
  </person>
  <person>
    <firstname>Barack</firstname>
    <lastname>Obama</lastname>
    <address>
      <street>1600 Pennsylvania Avenue</street>
      <city>Washington, D.C</city>
    </address>
  </person>
</people>
```