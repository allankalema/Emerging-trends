// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract StudentRecords {
    struct Student {
        string name;
        uint256 studentId;
    }

    mapping(address => Student) public students;

    event StudentRegistered(address indexed studentAddress, string name, uint256 studentId);

    function registerStudent(string memory _name, uint256 _studentId) public {
        students[msg.sender] = Student(_name, _studentId);
        emit StudentRegistered(msg.sender, _name, _studentId);
    }

    function getStudent(address _studentAddress) public view returns (string memory, uint256) {
        Student memory student = students[_studentAddress];
        return (student.name, student.studentId);
    }
}
